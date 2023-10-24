import os

import requests
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from conf import save_dir, token
from messages.pirate_find.pirate_find import pirate_show, too_match, shuffle, start_search, match_msg, profile_error, \
    contacts_sent
from messages.profile_set.profile_set_msgs import p_start_message, side_photo_message, name_message, info_message, \
    detail_message, char_message, status_message, name_except_message, info_exception_message, detail_exception_message, \
    status_exception_message, end_profile_flow, photo_exception, cancel_msg, cannot_cancel_msg, profile_show, \
    profile_delete
from models.db import User, engine
from photo_maker.add_text.add_text import add_text
from photo_maker.make_photo.make_photo import make_photo, stack_photo


def get_photo(data, postfix: str) -> str:
    photo = data['message']['photo'][-1]  # Получение последней (самой большой) фотографии
    file_id = photo['file_id']

    # Получение ссылки на файл фотографии
    photo_url = get_photo_url(file_id)

    if photo_url:
        # Загрузка фотографии на сервер Flask

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        uid = data['message']['from']['id']
        file_extension = photo_url.split('.')[-1]
        save_path = os.path.join(save_dir, f'{uid}_{postfix}.{file_extension}')

        response = requests.get(photo_url)

        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f'Фото успешно сохранено: {save_path}')
            return save_path
        else:
            raise Exception("Не удалось сохранить фото")


def get_photo_url(file_id):
    response = requests.get(f'https://api.telegram.org/bot{token}/getFile', params={'file_id': file_id})
    data = response.json()
    if 'result' in data and 'file_path' in data['result']:
        file_path = data['result']['file_path']
        photo_url = f'https://api.telegram.org/file/bot{token}/{file_path}'
        return photo_url
    else:
        return None


class UserInstance:
    id: int
    uid: str
    chat_id: int
    flow = ""
    stage = 0
    im_src1: str
    im_src2: str
    bg_src: str
    db_user = None
    seen_pirates = list()

    def __init__(self, iid, uid, chat_id):
        self.last_match = None
        self.id = iid
        self.uid = uid
        self.chat_id = chat_id
        self.seen_pirates = [self.id]

        self.has_profile = False
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(User).filter_by(id=self.id).first()
        session.commit()
        if user:
            self.has_profile = user.has_profile
        session.close()

    async def start_action(self, data):
        if self.flow:
            self.flows[self.flow][self.stage](self, data)
        else:
            pass

    def _get_side_photo(self, data):
        if 'message' in data and 'photo' in data['message']:
            self.im_src1 = get_photo(data, 'sd')
            self.making_photo = True
            make_photo(self.im_src1)
            self.image_with_bg = stack_photo(self.im_src1, self.im_src2, self.id)
            self.making_photo = False

            self.stage += 1
            name_message(self.chat_id)
        else:
            photo_exception(self.chat_id)

    def _get_front_photo(self, data):
        if 'message' in data and 'photo' in data['message']:
            self.im_src2 = get_photo(data, 'fr')
            self.making_photo = True
            make_photo(self.im_src2)
            self.making_photo = False

            self.stage += 1
            side_photo_message(self.chat_id)
        else:
            photo_exception(self.chat_id)

    def _validate_name(self, text: str):
        if text.isalpha() and len(text) <= 12:
            return True
        else:
            name_except_message(self.chat_id)
            return False

    def _get_name(self, data):
        try:
            if 'text' in data['message']:
                text = data['message']['text']
                text = text.split(' ')
                name = text[0]
                surname = text[1]

                if self._validate_name(name) and self._validate_name(surname):
                    self.name = name.upper()
                    self.surname = surname.upper()

                    info_message(self.chat_id)
                    self.stage += 1

        except Exception as ex:
            name_except_message(self.chat_id)

    def _validate_info(self, text: str):
        if len(text) <= 36:
            if not text.endswith('.'):
                text += "."
            return text
        info_exception_message(self.chat_id)
        return False

    def _get_info(self, data):
        try:
            if 'text' in data['message']:
                text = data['message']['text']
                text = self._validate_info(text)
                if text:
                    self.info = text.upper()
                    detail_message(self.chat_id)
                    self.stage += 1

        except Exception as ex:
            info_exception_message(self.chat_id)

    def _validate_detail(self, text: str):
        if len(text) <= 70:
            if not text.endswith('.'):
                text += "."
            if len(text) > 32:
                text = text.split(" ")
                length = 0
                for i, word in enumerate(text):
                    length += len(word)
                    if length > 32:
                        return "  ".join(text[:i]) + "\n" + "  ".join(text[i:])
            return text
        detail_exception_message(self.chat_id)
        return False

    def _get_detail(self, data):
        # try:
        if 'text' in data['message']:
            text = data['message']['text']
            text = self._validate_detail(text)
            if text:
                self.detail = text.upper()
                char_message(self.chat_id)
                self.stage += 1

        # except Exception as ex:
        #     detail_exception_message(self.chat_id)

    def _validate_behaviour(self, text: str):
        if len(text) <= 25:
            if not text.endswith('.'):
                text += "."
            return text
        info_exception_message(self.chat_id)
        return False

    def _get_behavior(self, data):
        try:
            if 'text' in data['message']:
                text = data['message']['text']
                text = self._validate_behaviour(text)
                if text:
                    self.beh = "ХАРАКТЕР   " + text.upper()
                    status_message(self.chat_id)
                    self.stage += 1
        except Exception as ex:
            detail_exception_message(self.chat_id)

    def _validate_status(self, text: str):
        if len(text) <= 25:
            if not text.endswith('.'):
                text += "."
            return text
        status_exception_message(self.chat_id)
        return False

    def _get_social_status(self, data):
        # try:
        if 'text' in data['message']:
            text = data['message']['text']
            text = self._validate_status(text)
            if text:
                self.status = text.upper()
                to_write = {
                    'name': self.name,
                    'surname': self.surname,
                    'info': self.info,
                    'descr': self.detail,
                    'beh': self.beh,
                    'status': self.status
                }
                add_text(self.image_with_bg, to_write)

                Session = sessionmaker(bind=engine)
                session = Session()
                user = session.query(User).filter_by(id=self.id).first()

                if not user:
                    new_user = User(id=self.id, username=self.uid, profile_picture=self.image_with_bg,
                                    chat_id=self.chat_id, has_profile=True)
                    session.add(new_user)
                else:
                    user.profile_picture = self.image_with_bg
                session.commit()
                session.close()
                self.has_profile = True
                end_profile_flow(self.chat_id, self.image_with_bg)

                self.end_flow()
        # except Exception as ex:
        #     detail_exception_message(self.chat_id)

    def start_profile_flow(self):
        self.flow = 'set_profile'
        self.stage = 0
        p_start_message(self.chat_id)

    def end_flow(self):
        self.flow = ''
        self.stage = 0

    def cancel(self):
        if self.flow:
            self.end_flow()
            cancel_msg(self.chat_id)
        else:
            cannot_cancel_msg(self.chat_id)

    def get_pirate(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(User).filter_by(id=self.id).first()

        if user and self.has_profile:
            start_search(self.chat_id)

            random_user = session.query(User).filter(User.has_profile == True, ~User.id.in_(self.seen_pirates)) \
                .order_by(func.random()).first()
            if random_user:

                pirate_show(self.chat_id, random_user)
                self.seen_pirates.append(random_user.id)
                self.last_match = random_user.id
            else:
                too_match(self.chat_id)
        else:
            profile_error(self.chat_id)

    def shuffle(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(User).filter_by(id=self.id).first()

        if user and self.has_profile:
            self.seen_pirates = [self.id]
            shuffle(self.chat_id)
        else:
            profile_error(self.chat_id)

    def match(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(User).filter_by(id=self.id).first()
        match_user = session.query(User).filter_by(id=self.last_match).first()

        if user and self.has_profile:
            if self.last_match:
                u_chat = match_user.chat_id
                match_msg(u_chat, user.username, user.profile_picture)
                contacts_sent(self.chat_id)
        else:
            profile_error(self.chat_id)

    def view_profile(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(User).filter_by(id=self.id).first()
        if user and self.has_profile:
            profile_show(self.chat_id, user.profile_picture)
        else:
            profile_error(self.chat_id)

    def set_chat_id(self, chat_id):
        self.chat_id = chat_id

    def delete_profile(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        user = session.query(User).filter_by(id=self.id).first()

        if user and self.has_profile:
            if os.path.exists(user.profile_picture):
                os.remove(user.profile_picture)
            user.profile_picture = ""
            user.has_profile = False
            self.has_profile = False
            profile_delete(self.chat_id)
        else:
            profile_error(self.chat_id)

    flows = {
        'set_profile': (
            _get_front_photo,
            _get_side_photo,
            _get_name,
            _get_info,
            _get_detail,
            _get_behavior,
            _get_social_status
        )
    }

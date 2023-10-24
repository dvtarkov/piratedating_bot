from messages.send_msg import send_message


def cancel_msg(chat_id):
    method = "sendMessage"
    text = "Заполнение профиля отменено!"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    send_message(method, data=data)


def cannot_cancel_msg(chat_id):
    method = "sendMessage"
    text = "Нет запущенных задач."
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    send_message(method, data=data)


def photo_exception(chat_id):
    method = "sendDocument"

    text = "*Где фото, Билли?! Нам нужно фото!*"
    files = {'document': open('imgs/send_photo.gif', 'rb')}
    data = {"chat_id": chat_id, "caption": text, "parse_mode": "Markdown"}
    send_message(method, data=data, files=files)


def p_start_message(chat_id):
    method = "sendPhoto"
    text = "Для начала заполнения профиля сфотографируйтесь смотря прямо в камеру и пришлите фото сюда.\n\n" \
           "Для большей правдоподобности обрежьте ваше фото примерно до 3:4."
    files = {'photo': open("imgs/p_front.jpg", 'rb')}
    data = {"chat_id": chat_id, "caption": text, "parse_mode": "Markdown"}
    send_message(method, data=data, files=files)


def side_photo_message(chat_id):
    method = "sendPhoto"
    text = "Теперь пришлите фото сбоку. СМОТРИТЕ ВПРАВО!\n\n" \
           "Для большей правдоподобности обрежьте ваше фото примерно до 3:4."
    files = {'photo': open("imgs/p_side.jpg", 'rb')}
    data = {"chat_id": chat_id, "caption": text, "parse_mode": "Markdown"}
    send_message(method, data=data, files=files)


def name_message(chat_id):
    method = "sendMessage"
    text = "Введите ваше имя и фамилию через пробел. *И имя, и фамилия*" \
           " не должны быть длиннее 12 символов.\nНапример: `ДЖОН СИЛЬВЕР`"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    send_message(method, data=data)


def name_except_message(chat_id):
    method = "sendMessage"
    text = "И имя и фамилия должны быть меньше 12 символов и содержать только буквы!"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    send_message(method, data=data)


def info_message(chat_id):
    method = "sendMessage"
    text = "Введите информацию о себе не более чем на 36 символов\nНапример: `ОЧЕНЬ, ОЧЕНЬ ХОРОШИЙ МАЛЬЧИК.`"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    send_message(method, data=data)


def info_exception_message(chat_id):
    method = "sendMessage"
    text = "Не более чем на 36 символов!"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    send_message(method, data=data)


def detail_message(chat_id):
    method = "sendMessage"
    text = "Напишите факт о себе не более чем на 70 символов\n" \
           "Например: `ОБЛАДАТЕЛЬ КАРТЫ ОСТРОВА СОКРОВИЩ. МНОГО ПЬЁТ И ВСЕГДА ПРОСТУЖЕН.`"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    send_message(method, data=data)


def detail_exception_message(chat_id):
    method = "sendMessage"
    text = "Не более чем на 70 символов! Или у вас очень длинные слова."
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    send_message(method, data=data)


def char_message(chat_id):
    method = "sendMessage"
    text = "Опишите ваш характер в двух словах, до 25 символов.\n" \
           "Например: `СКВЕРНЫЙ.`"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    send_message(method, data=data)


def char_exception_message(chat_id):
    method = "sendMessage"
    text = "До 25 символов!"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    send_message(method, data=data)


def status_exception_message(chat_id):
    method = "sendMessage"
    text = "До 20 символов!"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    send_message(method, data=data)


def status_message(chat_id):
    method = "sendMessage"
    text = "Опишите своё семейное положение, до 20 символов.\n" \
           "Например: `НЕ ЖЕНАТ.`"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    send_message(method, data=data)


def end_profile_flow(chat_id, src_file):
    method = "sendPhoto"
    text = "Ваш профиль был создан! Начните искать других пиратов прямо сейчас!\nВведите команду /find"
    files = {'photo': open(src_file, 'rb')}
    data = {"chat_id": chat_id, "caption": text, "parse_mode": "Markdown"}
    send_message(method, data=data, files=files)


def p_cancel(chat_id):
    method = "sendMessage"
    text = "Процесс создания профиля прерван."
    data = {"chat_id": chat_id, "caption": text, "parse_mode": "Markdown"}
    send_message(method, data=data)


def profile_show(chat_id, src_file):
    method = "sendPhoto"
    text = "Ваш профиль был создан! Начните искать других пиратов прямо сейчас!" \
           "\nВведите команду /find"
    files = {'photo': open(src_file, 'rb')}
    data = {"chat_id": chat_id, "caption": text, "parse_mode": "Markdown"}
    send_message(method, data=data, files=files)


def profile_delete(chat_id):
    method = "sendPhoto"
    text = "Мы успешно удалили ваш профиль! Но вы можете сделать новый по команде /setprofile"
    files = {'photo': open("imgs/delete.jpg", 'rb')}
    data = {"chat_id": chat_id, "caption": text, "parse_mode": "Markdown"}
    send_message(method, data=data, files=files)


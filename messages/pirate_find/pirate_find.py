from messages.send_msg import send_message


def start_search(chat_id):
    method = "sendDocument"
    text = "Начинаем поиск."
    files = {'document': open("imgs/searching.gif", 'rb')}
    data = {"chat_id": chat_id, "caption": text, "parse_mode": "Markdown"}
    send_message(method, data=data, files=files)


def pirate_show(chat_id, user):
    src_file = user.profile_picture

    method = "sendPhoto"

    text = "Вы кого-то нашли! Хотите отправить ему свой контакт?\nВведите: /sendcontact\n" \
           "Чтобы продолжить поиск введите: /find"
    files = {'photo': open(src_file, 'rb')}
    print(files)
    data = {"chat_id": chat_id, "caption": text, "parse_mode": "Markdown"}
    print(data)
    send_message(method, data=data, files=files)


def too_match(chat_id):
    method = "sendDocument"
    text = "Кажется пираты кончились. Если вы хотите пойти по второму кругу введите /shuffle"
    files = {'document': open("imgs/too_match.gif", 'rb')}
    data = {"chat_id": chat_id, "caption": text, "parse_mode": "Markdown"}
    send_message(method, data=data, files=files)


def shuffle(chat_id):
    method = "sendDocument"
    text = "Пираты пошли по второму кругу! Введите /find чтобы начать их искать."
    files = {'document': open("imgs/shuffle.gif", 'rb')}
    data = {"chat_id": chat_id, "caption": text, "parse_mode": "Markdown"}
    send_message(method, data=data, files=files)


def contacts_sent(chat_id):
    method = "sendDocument"
    text = "Ваши контакты отправлены! Введите /find чтобы продолжить поиски."
    files = {'document': open("imgs/contacts_sent.gif", 'rb')}
    data = {"chat_id": chat_id, "caption": text, "parse_mode": "Markdown"}
    send_message(method, data=data, files=files)


def match_msg(chat_id, uid, src_file):
    method = "sendPhoto"
    text = f"Этот пират хочет познакомиться с вами!\n\nНапишите ему: @{uid}"
    files = {'photo': open(src_file, 'rb')}
    data = {"chat_id": chat_id, "caption": text, "parse_mode": "Markdown"}
    send_message(method, data=data, files=files)


def profile_error(chat_id):
    method = "sendMessage"
    text = f"Для начала поиска заполните профиль!\n\n/set_profile"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    send_message(method, data=data)

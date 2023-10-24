from messages.send_msg import send_message


def start_message(chat_id):
    method = "sendMessage"
    text = "Добро пожаловать на борт!\n" \
           "Здесь вы можете создать анкету в стиле Острова Сокровищ и отправиться на поиски товарищей.\n" \
           "Введите /setprofile для начала создания анкеты." \

    data = {"chat_id": chat_id, "text": text}
    send_message(method, data=data)


def help_message(chat_id):
    method = "sendMessage"
    text = "*Краткая помощь:*\n" \
           "/start - приветственное сообщение.\n" \
           "/setprofile - создать/изменить профиль.\n" \
           "/cancel - отменить создание профиля.\n\n" \
           "*Только после создания профиля:*\n" \
           "/viewprofile - посмотреть свой профиль.\n" \
           "/find - найти пирата.\n" \
           "/shuffle - начать поиск заново.\n" \
           "/deleteprofile - чтобы удалить профиль."
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    send_message(method, data=data)

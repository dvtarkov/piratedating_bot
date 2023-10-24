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
    text = "help text"
    data = {"chat_id": chat_id, "text": text}
    send_message(method, data=data)

import requests

from conf import token
from instanses import UserInstance
from processors import user_processors


def get_user_processor(data):
    iid = data['message']['from']['id']
    uid = data['message']['from']['username']
    chat_id = data["message"]["chat"]["id"]
    if iid not in user_processors:
        user_processors[iid] = UserInstance(iid, uid, chat_id)
        return user_processors[iid]
    else:
        return user_processors[iid]

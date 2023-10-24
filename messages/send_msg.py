import requests

from conf import token


def send_message(method, **kwargs):
    url = f"https://api.telegram.org/bot{token}/{method}"
    print(requests.post(url, **kwargs).text)

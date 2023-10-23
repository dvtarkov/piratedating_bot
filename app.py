from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/your-webhook-url', methods=['POST'])
def webhook():
    data = request.get_json()
    # Обработка данных от телеграм-бота здесь
    return 'OK'


if __name__ == '__main__':
    app.run()

import asyncio

from commands.commands_handlers import commands
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import models.db
from utils import get_user_processor

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
# db = SQLAlchemy(app)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/webhook', methods=['POST'])
def webhook():
    asyncio.run(handle_message(request))
    return "Ok"


async def handle_message(user_request):
    data = user_request.json

    print(data)
    if 'message' in data:
        if 'text' in data['message'].keys() and data['message']['text'] in commands:
            commands[data['message']['text']](data)
        else:
            u_proc = get_user_processor(data)
            asyncio.create_task(u_proc.start_action(data))

if __name__ == '__main__':
    app.run(debug=True)

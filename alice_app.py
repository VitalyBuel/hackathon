# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с логами.
import logging

# Импортируем модуль для работы с API Алисы
from alice_sdk import AliceRequest, AliceResponse

# Импортируем модуль с логикой игры
from main import handle_dialog

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)


#logging.basicConfig(level=logging.DEBUG)
app.config['SECRET_KEY'] = 'alice'
logging.basicConfig(
    filename='example.log',
    format='%(asctime)s %(name)s %(message)s',
    level=logging.INFO
    )

# Хранилище данных о сессиях.
session_storage = {}


# Задаем параметры приложения Flask.
@app.route("/alice", methods=['POST'])
def main():
    # Функция получает тело запроса и возвращает ответ.
    alice_request = AliceRequest(request.json)
    logging.info('Request: {}'.format(alice_request))

    alice_response = AliceResponse(alice_request)

    user_id = alice_request.user_id

    alice_response, session_storage[user_id] = handle_dialog(
        alice_request, alice_response, session_storage.get(user_id)
    )

    logging.info('Response: {}'.format(alice_response))

    return alice_response.dumps()


if __name__ == '__main__':
    app.run('0.0.0.0', port=2000, debug=True)

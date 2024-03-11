from datetime import datetime

import requests
from _decimal import Decimal

from django.shortcuts import render

from ticket_tracking.models import Event


def test_request(request):
    bot_token = '6515402227:AAHxB2hDjHzZ9fX2jDlFRE__R0lb5yUiwA0'
    base_url = f'https://api.telegram.org/bot{bot_token}/'
    # Замініть 'text' на текст повідомлення, яке ви хочете відправити
    message_text = 'Привіт, це тестове повідомлення від вашого бота!'

    # Формування URL для надсилання повідомлення
    send_message_url = f'{base_url}sendMessage'
    chat_id = 772530745
    # Параметри POST-запиту для надсилання повідомлення
    params = {'chat_id': chat_id, 'text': message_text}

    # Відправлення POST-запиту
    response = requests.post(send_message_url, data=params)

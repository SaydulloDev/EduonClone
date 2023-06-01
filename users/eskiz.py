import os
from pathlib import Path

import environ
import requests

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


def get_token():
    email = env('EMAIL_SMS')
    password = env('SECRET_KEY_SMS')
    BASE_URL = 'https://notify.eskiz.uz/api/auth/login'
    request_body = {
        'email': email,
        'password': password
    }
    token = requests.post(url=BASE_URL, data=request_body).json()
    token = token.get('data').get('token')
    return token


def send_verify_code(phone, code):
    BASE_URL = 'https://notify.eskiz.uz/api/message/sms/send'
    request_data = {
        'mobile_phone': phone,
        'message': code,
        'from': '4546'
    }
    request_header = {
        'Authorization': f'Bearer {get_token()}'
    }
    message = requests.post(url=BASE_URL, data=request_data, headers=request_header)
    return message

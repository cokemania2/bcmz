import requests
import hashlib
import hmac
import base64
import time
import json
from random import randint
from django.conf import settings


def make_signature():
    time_stamp = str(int(time.time() * 1000))
    access_key = settings.ACCESS_KEY				            # access key id (from portal or Sub Account)
    secret_key = bytes(settings.SCREPT_KEY, 'UTF-8')			# secret key (from portal or Sub Account)
    method = "POST"
    uri = f"/sms/v2/services/{settings.SMS_APP_KEY}/messages"
    message = bytes(method + " " + uri + "\n" + time_stamp + "\n" + access_key, 'UTF-8')

    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey


def send_meesage():
    time_stamp = str(int(time.time() * 1000))

    url = f"https://sens.apigw.ntruss.com/sms/v2/services/{settings.SMS_APP_KEY}/messages"
    headers = {'Content-Type': 'application/json; charset=utf-8',
               'x-ncp-apigw-timestamp': time_stamp,
               'x-ncp-iam-access-key': settings.ACCESS_KEY,
               'x-ncp-apigw-signature-v2': make_signature()}
    number = randint(1000, 10000)
    message = f"SMS인증번호는 {number} 입니다. 인증번호를 정확히 입력해주세요."		# 메세지 내용을 저장
    phone = "01020647744"			# 핸드폰 번호를 저장

    body = {
        "type": "SMS",
        "contentType": "COMM",
        "from": "01020647744",
        "content": message,
        "messages": [{"to": phone}]
    }
    body = json.dumps(body)
    if settings.PRODUCTION:
        res = requests.post(url, data=body, headers=headers)
        if res.status_code == 202:
            return number
    else:
        print(f'인증번호  = {number}')
        return number
    return 0


def make_hash(data):
    data_hash = hashlib.new('sha256')
    data_hash.update(data.encode('utf-8'))
    return data_hash.hexdigest()

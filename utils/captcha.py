import json
import requests as r
from configs.captcha import CAPTCHA_SECRET

_CAPTCHA_URL = 'https://www.google.com/recaptcha/api/siteverify'

def verifyCaptcha(token: str = ''):
    response = r.post("{url}?secret={secret}&response={token}".format(url=_CAPTCHA_URL, secret=CAPTCHA_SECRET, token=token))
    res = json.loads(response.content, cls=json.JSONDecoder)
    return res['success']

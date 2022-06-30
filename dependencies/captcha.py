from typing import Union
from fastapi import HTTPException, Header, status

from utils.captcha import verifyCaptcha

def validateCaptcha(captcha: Union[str, None] = Header(default=None)):
    '''Dependency requiring valid captcha before proceeding.'''
    if not captcha or not len(captcha):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CAPTCHA required.")
    if not verifyCaptcha(token=captcha):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="CAPTCHA verification failed.")

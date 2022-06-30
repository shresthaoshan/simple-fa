from datetime import datetime
from typing import Union
from jose import jwt

_SECRET_KEY="28d5337052696989ce5da78631a25e9727a4595868a0bd0cd79bb6f75c852f12"
_ALGORITHM="HS512"

def get_access_token(payload: dict, expire_delta: Union[int, None]) -> str:
    _payload = payload.copy()
    if expire_delta:
        _payload.update({"exp": datetime.utcnow() + expire_delta}) # 2 minutes
    token = jwt.encode(claims=_payload, key=_SECRET_KEY, algorithm=_ALGORITHM)
    return token

def verify_access_token(token: str):
    payload: Union[dict, None] = jwt.decode(token=token, key=_SECRET_KEY, algorithms=[_ALGORITHM])
    return payload
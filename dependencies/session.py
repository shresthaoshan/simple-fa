from typing import Union

from fastapi import Cookie, HTTPException, status

from utils.token import verify_access_token

async def validate_session(session: Union[str, None] = Cookie(default=None)):
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session required.")
    try:
        return verify_access_token(session)
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session invalid.")
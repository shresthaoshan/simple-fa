from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Response, status

from dependencies import db, captcha
from dependencies.session import validate_session
from schemas.user import User, UserCreateBase, UserLoginBase
from crud.user import create_new_user, get_user_by_email
from utils.hash import verify_password
from utils.token import get_access_token

router = APIRouter(prefix="/auth")

_COOKIE_EXPIRE_DELTA=20 # minutes

@router.get("/")
def home():
    return {'check': True}

@router.get("/token", response_model=User)
def refresh(response: Response, payload: dict = Depends(validate_session)):
    if "exp" in payload:
        payload.pop("exp")
    token = get_access_token(payload=payload)
    response.set_cookie("session", token, max_age=timedelta(minutes=2), httponly=True)
    return payload

@router.post("/register", response_model=User, dependencies=[Depends(captcha.validateCaptcha)])
async def register(user: UserCreateBase, response: Response, db: Session = Depends(db.get_db)):
    user_exists = get_user_by_email(db, user.email)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists.")
    new_user = create_new_user(db, user)
    token = get_access_token(new_user.to_dict())
    response.set_cookie("session", token, max_age=timedelta(minutes=_COOKIE_EXPIRE_DELTA), httponly=True)
    return new_user

@router.post("/signin", response_model=User, dependencies=[Depends(captcha.validateCaptcha)])
async def login(user: UserLoginBase, response : Response, db: Session = Depends(db.get_db)):
    user_exists = get_user_by_email(db, user.email)
    if not user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Credentials invalid.")
    if not verify_password(user_exists.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Credentials invalid.")
    token = get_access_token(user_exists.to_dict())
    response.set_cookie("session", token, max_age=timedelta(minutes=_COOKIE_EXPIRE_DELTA), httponly=True)
    return user_exists

@router.post("/signout", dependencies=[Depends(validate_session)])
def logout(response: Response):
    response.delete_cookie("session")
    return dict(success=True)
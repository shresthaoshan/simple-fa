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

@router.get("/")
def home():
    return {'check': True}

@router.get("/refresh", response_model=User)
def refresh(response: Response, payload: dict = Depends(validate_session)):
    payload.pop("exp")
    token = get_access_token(payload=payload)
    response.set_cookie("session", token, max_age=timedelta(minutes=2), httponly=True)
    return payload

@router.post("/register", response_model=User, dependencies=[Depends(captcha.validateCaptcha)])
async def register(user: UserCreateBase, db: Session = Depends(db.get_db)):
    user_exists = get_user_by_email(db, user.email)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists.")
    return create_new_user(db, user)

@router.post("/login", response_model=User, dependencies=[Depends(captcha.validateCaptcha)])
async def login(user: UserLoginBase, response : Response, db: Session = Depends(db.get_db)):
    user_exists = get_user_by_email(db, user.email)
    if not user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Credentials invalid.")
    if not verify_password(user_exists.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Credentials invalid.")
    token = get_access_token(user_exists.to_dict())
    response.set_cookie("session", token, max_age=timedelta(minutes=2), httponly=True)
    return user_exists
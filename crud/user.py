from sqlalchemy.orm import Session

from schemas import user as schema
from models.user import User
from utils.hash import hash_password

def get_user(db: Session, id: int) -> User | None:
    return db.query(User).filter(User.id == id).first()

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def create_new_user(db: Session, user: schema.UserCreateBase):
    db_user = User(full_name=user.full_name, email=user.email, password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
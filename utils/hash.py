from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(hash: str, password: str):
    return _pwd_context.verify(password, hash)

def hash_password(password: str):
    return _pwd_context.hash(password)
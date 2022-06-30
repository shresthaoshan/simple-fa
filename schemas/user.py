from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserLoginBase(UserBase):
    password: str

class UserCreateBase(UserLoginBase):
    full_name: str

class User(UserBase):
    id: int
    full_name: str

    class Config:
        orm_mode = True
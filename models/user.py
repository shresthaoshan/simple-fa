from sqlalchemy import Column, Integer, String
from db.core import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    password = Column(String)

    def to_dict(self):
        return {"id": self.id, "full_name": self.full_name, "email": self.email}
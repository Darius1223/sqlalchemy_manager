from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    first_name = Column(String)

from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    money = Column(Integer, default=0)


class ChatMember(Base):
    __tablename__ = "chatmember"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    user_id = Column(Integer)
    warns = Column(Integer, default=0)

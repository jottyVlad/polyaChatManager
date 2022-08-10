from sqlalchemy import Column, Integer, Boolean
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


class ChatSettings(Base):
    __tablename__ = "chatsettings"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)

    roleplay_enabled = Column(Boolean, default=True)
    nsfw_enabled = Column(Boolean, default=False)

    def __getitem__(self, item):
        if not hasattr(self, item):
            raise KeyError
        return getattr(self, item)

    def __setitem__(self, key, value):
        if not hasattr(self, key):
            raise KeyError
        setattr(self, key, value)

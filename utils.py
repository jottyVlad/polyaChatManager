from sqlmodel import create_engine, SQLModel, Session, select

from globals import Globals
from models import ChatMember, User, ChatSettings


def init_db():

    engine = create_engine("sqlite:///bot.db")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.commit()

    return engine


def get_chatmember_or_none(chat_id: int,
                           user_id: int
                           ) -> ChatMember | None:

    engine = Globals.db_engine
    with Session(engine) as session:
        statement = select(ChatMember).where(ChatMember.chat_id == chat_id,
                                             ChatMember.user_id == user_id)
        chat_member = session.exec(statement).first()
    return chat_member


async def create_chatmember(chat_id: int,
                            user_id: int,
                            warns: int = 0) -> ChatMember:
    engine = Globals.db_engine
    with Session(engine) as session:
        chat_member = ChatMember(chat_id=chat_id,
                                 user_id=user_id,
                                 warns=warns)
        session.add(chat_member)
        session.commit()
    return chat_member


def get_user_or_none(user_id: int) -> User | None:
    engine = Globals.db_engine
    with Session(engine) as session:
        statement = select(User).where(User.user_id == user_id)
        user = session.exec(statement).first()
    return user


def create_user(user_id: int) -> User | None:
    engine = Globals.db_engine
    with Session(engine) as session:
        user = User(user_id=user_id)
        session.add(user)
        session.commit()
    return user


def get_chatsettings_or_none(chat_id: int) -> ChatSettings | None:
    engine = Globals.db_engine
    with Session(engine) as session:
        statement = select(ChatSettings).where(
            ChatSettings.chat_id == chat_id
        )
        chatsettings = session.exec(statement).first()
    return chatsettings


def create_chatsettings(chat_id: int) -> ChatSettings | None:
    engine = Globals.db_engine
    with Session(engine) as session:
        chatsettings = ChatSettings(chat_id=chat_id)
        session.add(chatsettings)
        session.commit()
    return chatsettings


def save_model(model: SQLModel) -> None:
    engine = Globals.db_engine
    with Session(engine) as session:
        session.add(model)
        session.commit()
        session.refresh(model)
    return None

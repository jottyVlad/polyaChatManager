from sqlmodel import create_engine, SQLModel, Session, select

from globals import Globals
from models import ChatMember


# def get_all_models() -> list:
#     import sys
#     import inspect
#     classes = inspect.getmembers(sys.modules["models"], inspect.isclass)
#     classes = [a[1] for a in classes if a[0] != "BaseModel"]
#     return classes


def init_db():

    engine = create_engine("sqlite:///bot.db")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.commit()

    return engine


def get_chatmember_or_none(chat_id: int,
                           user_id: int
                           ) -> ChatMember:

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


async def save_model(model: SQLModel) -> None:
    engine = Globals.db_engine
    with Session(engine) as session:
        session.add(model)
        session.commit()
        session.refresh(model)
    return None

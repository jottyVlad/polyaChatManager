from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

from models import ChatMember
from repositories.base_repository import BaseRepository


class ChatMemberRepository(BaseRepository):
    def create(self, chat_id: int, user_id: int, warns: int = 0):
        try:
            statement = (insert(ChatMember).
                         values(chat_id=chat_id,
                                user_id=user_id,
                                warns=warns))
            self.session.execute(statement)
            self.session.commit()
        except:  # noqa
            self.session.rollback()
            raise ValueError("Can't create chatmember object")

    def get(self, chat_id: int, user_id: int):
        try:
            statement = (select(ChatMember).
                         where(ChatMember.chat_id == chat_id,
                               ChatMember.user_id == user_id))

            result = self.session.execute(statement).scalar()
        except:  # noqa
            raise ValueError
        return result

    def save(self, chatmember: ChatMember):
        try:
            self.session.add(chatmember)
            self.session.commit()
        except: # noqa
            self.session.rollback()
            raise ValueError("Can't save ChatMember object")


    def change_warns(self, chat_id: int, user_id: int, warns: int):
        try:
            statement = (update(ChatMember).
                         where(ChatMember.chat_id == chat_id,
                               ChatMember.user_id == user_id).
                         values(warns=warns))
            self.session.execute(statement)
            self.session.commit()
        except:  # noqa
            self.session.rollback()
            raise ValueError("Can't change ChatMember's warns")

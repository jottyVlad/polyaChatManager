from sqlalchemy import update

from models import ChatMember
from repositories.base_repository import BaseRepository
from repositories.operations import CreateOperationMixin, \
    GetOperationMixin, \
    SaveOperationMixin


class ChatMemberRepository(BaseRepository,
                           CreateOperationMixin,
                           GetOperationMixin,
                           SaveOperationMixin):
    model = ChatMember

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

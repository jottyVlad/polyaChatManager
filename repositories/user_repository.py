from sqlalchemy import insert, select

from models import User
from repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def create(self, user_id: int, money: int = 0):
        try:
            statement = (insert(User).
                         values(user_id=user_id, money=money))
            self.session.execute(statement)
            self.session.commit()
        except:  # noqa
            self.session.rollback()
            raise ValueError("Can't create user object")

    def get(self, user_id: int):
        try:
            statement = select(User).where(User.user_id == user_id)
            result = self.session.execute(statement).scalar()
        except:  # noqa
            raise ValueError

        return result

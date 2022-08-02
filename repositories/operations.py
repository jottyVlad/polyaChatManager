from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import DeclarativeMeta, Session

DeclarativeMetaType = TypeVar('DeclarativeMetaType', bound=DeclarativeMeta)


class BaseOperation(Generic[DeclarativeMetaType]):
    model: DeclarativeMetaType
    session: Session


class CreateOperationMixin(BaseOperation):

    def create(self, **kwargs):
        obj = self.model(**kwargs)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj


class GetOperationMixin(BaseOperation):

    def get(self, **kwargs):
        statement = (select(self.model).
                     filter_by(**kwargs))
        result = self.session.execute(statement).scalars().first()

        if not result:
            raise ValueError
        return result


class SaveOperationMixin(BaseOperation):

    def save(self, model_: DeclarativeMetaType):
        try:
            self.session.add(model_)
            self.session.commit()
        except:  # noqa
            self.session.rollback()
            raise ValueError(f"Can't save {model_.__tablename__} object")

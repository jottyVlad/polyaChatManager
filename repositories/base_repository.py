from abc import ABC, abstractmethod

from sqlalchemy.orm import Session


class BaseRepository(ABC):
    session: Session

    @abstractmethod
    def create(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get(self, **kwargs):
        raise NotImplementedError

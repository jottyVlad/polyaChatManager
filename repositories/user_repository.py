from models import User
from repositories.base_repository import BaseRepository
from repositories.operations import CreateOperationMixin, GetOperationMixin


class UserRepository(BaseRepository,
                     CreateOperationMixin,
                     GetOperationMixin):
    model = User

from models import ChatSettings
from repositories.base_repository import BaseRepository
from repositories.operations import CreateOperationMixin, \
    GetOperationMixin, \
    SaveOperationMixin


class ChatSettingsRepository(BaseRepository,
                             CreateOperationMixin,
                             GetOperationMixin,
                             SaveOperationMixin):
    model = ChatSettings

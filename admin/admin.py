from sqladmin import ModelView

from models import User, ChatMember, ChatSettings


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.user_id, User.money]


class ChatMemberAdmin(ModelView, model=ChatMember):
    column_list = [ChatMember.id,
                   ChatMember.chat_id,
                   ChatMember.user_id,
                   ChatMember.warns]


class ChatSettingsAdmin(ModelView, model=ChatSettings):
    column_list = [ChatSettings.id,
                   ChatSettings.chat_id,
                   ChatSettings.roleplay_enabled,
                   ChatSettings.nsfw_enabled]

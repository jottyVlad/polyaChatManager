from tortoise.models import Model
from tortoise import fields


class ChatMember(Model):
    id = fields.IntField(pk=True)
    chat_id = fields.IntField()
    user_id = fields.IntField()
    warns = fields.IntField(default=0)

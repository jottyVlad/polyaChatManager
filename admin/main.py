from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy import create_engine

from admin import UserAdmin, ChatMemberAdmin, ChatSettingsAdmin
from config import CONNECTION_STRING

engine = create_engine(
    CONNECTION_STRING,
    connect_args={"check_same_thread": False},
)

app = FastAPI()
admin = Admin(app, engine)

admin.add_view(UserAdmin)
admin.add_view(ChatMemberAdmin)
admin.add_view(ChatSettingsAdmin)

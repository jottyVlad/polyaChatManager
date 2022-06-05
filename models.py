from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int


class ChatMember(SQLModel, table=True):
    id: int = Field(primary_key=True)
    chat_id: int
    user_id: int
    warns: int

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int
    money: int = Field(default=0)


class ChatMember(SQLModel, table=True):
    id: int = Field(primary_key=True)
    chat_id: int
    user_id: int
    warns: int = Field(default=0)

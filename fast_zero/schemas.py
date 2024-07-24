from pydantic import BaseModel, ConfigDict, EmailStr

from fast_zero.models import TodoState


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublicSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserDB(UserSchema):
    id: int


class UserListSchema(BaseModel):
    users: list[UserPublicSchema]


class Message(BaseModel):
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoPulicSchema(TodoSchema):
    id: int


class TodoListPulicSchema(BaseModel):
    todos: list[TodoPulicSchema]


class TodoUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None


class TodoQuerySchema(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None
    offset: int = 0
    limit: int = 10

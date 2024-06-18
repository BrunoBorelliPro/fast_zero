from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import (
    Message,
    UserDB,
    UserListSchema,
    UserPublicSchema,
    UserSchema,
)

app = FastAPI()

database = []


@app.get('/')
def read_root():
    return {'message': 'Olar mundo!'}


@app.post(
    '/users/', status_code=HTTPStatus.CREATED, response_model=UserPublicSchema
)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)

    return user_with_id


@app.get('/users/', response_model=UserListSchema)
def read_users():
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublicSchema)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    del database[user_id - 1]

    return {'message': 'User deleted'}

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from fast_zero.models import Todo
from fast_zero.schemas import (
    TodoListPulicSchema,
    TodoPulicSchema,
    TodoQuerySchema,
    TodoSchema,
    TodoUpdateSchema,
)
from fast_zero.types import T_CurrentUser, T_Session

router = APIRouter(
    prefix='/todos',
    tags=['todos'],
)


@router.post(
    '/', response_model=TodoPulicSchema, status_code=HTTPStatus.CREATED
)
def create_todo(todo: TodoSchema, user: T_CurrentUser, session: T_Session):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get('/', response_model=TodoListPulicSchema)
def read_todos(
    user: T_CurrentUser,
    session: T_Session,
    params: TodoQuerySchema = Depends(TodoQuerySchema),
):
    query = select(Todo).where(Todo.user_id == user.id)

    if params.title:
        query = query.filter(Todo.title.contains(params.title))
    if params.description:
        query = query.filter(Todo.description.contains(params.description))
    if params.state:
        query = query.filter(Todo.state == params.state)

    query = query.offset(params.offset).limit(params.limit)

    todos = session.scalars(query)
    return {'todos': todos}


@router.delete('/{todo_id}', status_code=HTTPStatus.OK)
def delete_todo(todo_id: int, user: T_CurrentUser, session: T_Session):
    todo = session.scalar(
        select(Todo).where(
            Todo.user_id == user.id,
            Todo.id == todo_id,
        )
    )

    if todo is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Task not found.',
        )

    session.delete(todo)
    session.commit()
    return {'message': 'Task has been deleted successfully.'}


@router.patch('/{todo_id}', response_model=TodoPulicSchema)
def update_todo(
    user: T_CurrentUser,
    session: T_Session,
    todo_id: int,
    todo: TodoUpdateSchema,
):
    db_todo = session.scalar(
        select(Todo).where(
            Todo.user_id == user.id,
            Todo.id == todo_id,
        )
    )

    if db_todo is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Task not found.',
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.commit()
    session.refresh(db_todo)
    return db_todo

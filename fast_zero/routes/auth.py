from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from fast_zero.models import User
from fast_zero.security import (
    create_access_token,
    verify_password,
)
from fast_zero.types import T_CurrentUser, T_OAuth2Form, T_Session

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/token/')
def login_for_access_token(
    form_data: T_OAuth2Form,
    session: T_Session,
):
    user = session.scalar(select(User).where(User.email == form_data.username))
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )
    access_token = create_access_token({'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/refresh_token/')
def refresh_access_token(
    user: T_CurrentUser,
):
    new_access_token = create_access_token({'sub': user.email})
    return {'access_token': new_access_token, 'token_type': 'bearer'}

from http import HTTPStatus

import pytest
from fastapi import HTTPException
from jwt import decode

from fast_zero.security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    get_current_user,
)


def test_create_access_token():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)

    result = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert result['sub'] == data['sub']
    assert result['exp']


def test_get_current_user(session, token, user):
    result = get_current_user(session=session, token=token)

    assert result.id == user.id


def test_get_current_user__invalid_token(session):
    token = 'invalid_token'

    with pytest.raises(HTTPException):
        get_current_user(session=session, token=token)


def test_get_current_user__without_sub(session):
    access_token = create_access_token({'sub': ''})

    with pytest.raises(HTTPException):
        get_current_user(session=session, token=access_token)


def test_get_current_user__without_email(session):
    access_token = create_access_token({'sub': 'fake@email.com'})

    with pytest.raises(HTTPException):
        get_current_user(session=session, token=access_token)


def test_jwt__invalid_token(client, user):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': 'Bearer invalid_token'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt__without_sub(client, user):
    access_token = create_access_token({'sub': ''})

    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt__without_email(client, user):
    access_token = create_access_token({'sub': 'emailfake@email.com'})

    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}

from http import HTTPStatus

from fast_zero.schemas import UserPublicSchema


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'email': 'email@email.com',
            'password': 'password',
            'username': 'username',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'email': 'email@email.com',
        'username': 'username',
        'id': 1,
    }
    assert response.json().get('password') is None


def test_create_user__username_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'email': 'email@email.com',
            'password': 'password',
            'username': user.username,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_user__email_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'email': user.email,
            'password': 'password',
            'username': 'username',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user, other_user):
    user_schema = UserPublicSchema.model_validate(user).model_dump()
    other_user_schema = UserPublicSchema.model_validate(
        other_user
    ).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema, other_user_schema]}


def test_get_user(client):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_user_with_user(client, user):
    user_schema = UserPublicSchema.model_validate(user).model_dump()
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        json={
            'email': 'email2@email.com',
            'username': 'username',
            'password': user.clean_password,
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'email': 'email2@email.com',
        'username': 'username',
        'id': 1,
    }
    assert response.json().get('password') is None


def test_update_user__user_is_not_the_owner_of_the_user(
    client, user, other_user, token
):
    response = client.put(
        f'/users/{other_user.id}',
        json={
            'email': 'email@email.com',
            'username': 'username',
            'password': 'password',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}


def test_update_user__username_already_exists(client, user, other_user, token):
    response = client.put(
        f'/users/{user.id}',
        json={
            'email': 'email@email.com',
            'username': other_user.username,
            'password': 'password',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_update_user__email_already_exists(client, user, other_user, token):
    response = client.put(
        f'/users/{user.id}',
        json={
            'email': other_user.email,
            'username': 'username',
            'password': 'password',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_update_user_just_change_username(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'username',
            'password': user.clean_password,
            'email': user.email,
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'email': user.email,
        'username': 'username',
        'id': 1,
    }
    assert response.json().get('password') is None


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user__user_is_not_the_owner_of_the_user(
    client, other_user, token
):
    response = client.delete(
        f'/users/{other_user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}

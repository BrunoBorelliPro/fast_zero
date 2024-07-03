from http import HTTPStatus

from fast_zero.schemas import UserPublicSchema


def test_read_root_deve_retornar_ok_e_olar_mundo(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olar mundo!'}


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


def test_read_users_with_user(client, user):
    user_schema = UserPublicSchema.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


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
            'password': 'password',
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


def test_update_user__user_is_not_the_owner_of_the_user(client, user, token):
    response = client.put(
        '/users/2',
        json={
            'email': 'email@email.com',
            'username': 'username',
            'password': 'password',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Not enough permission'}


def test_update_user__username_already_exists(client, user, user2, token):
    response = client.put(
        f'/users/{user.id}',
        json={
            'email': 'email@email.com',
            'username': user2.username,
            'password': 'password',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_update_user__email_already_exists(client, user, user2, token):
    response = client.put(
        f'/users/{user.id}',
        json={
            'email': user2.email,
            'username': 'username',
            'password': 'password',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user__user_is_not_the_owner_of_the_user(client, user, token):
    response = client.delete(
        '/users/2', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Not enough permission'}


def test_token(client, user):
    response = client.post(
        '/token/',
        data={
            'username': user.email,
            'password': user.clean_password,  # Here we are using the clean pwd
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json().get('access_token')
    assert response.json().get('token_type') == 'bearer'


def test_token__user_not_found(client):
    response = client.post(
        '/token/',
        data={
            'username': 'email',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token__incorrect_password(client, user):
    response = client.post(
        '/token/',
        data={
            'username': user.email,
            'password': user.password,  # Here we are using the hashed pwd
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}

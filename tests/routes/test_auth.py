from http import HTTPStatus

from freezegun import freeze_time


def test_token(client, user):
    response = client.post(
        '/auth/token/',
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
        '/auth/token/',
        data={
            'username': 'email',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token__incorrect_password(client, user):
    response = client.post(
        '/auth/token/',
        data={
            'username': user.email,
            'password': user.password,  # Here we are using the hashed pwd
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token__incorrect_email(client, user):
    response = client.post(
        '/auth/token/',
        data={
            'username': 'email',
            'password': user.clean_password,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_expired_after_time(client, user):
    with freeze_time('2021-01-01 12:00:00'):
        # Gera o token 12:00
        response = client.post(
            '/auth/token/',
            data={
                'username': user.email,
                'password': user.clean_password,
            },
        )
        token = response.json().get('access_token')

    with freeze_time('2021-01-01 12:31:00'):
        # Tenta usar o token 12:31
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'email': user.email,
                'username': user.username,
                'password': user.clean_password,
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_refresh_token(client, token):
    response = client.post(
        '/auth/refresh_token/',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


def test_refresh_token__no_token(client):
    response = client.post(
        '/auth/refresh_token/',
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_refresh_token__invalid_token(client):
    response = client.post(
        '/auth/refresh_token/',
        headers={'Authorization ': 'Bearer invalid_token'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_refresh_token__expired_token(client, user):
    with freeze_time('2021-01-01 12:00:00'):
        response = client.post(
            '/auth/token/',
            data={
                'username': user.email,
                'password': user.clean_password,
            },
        )
        token = response.json().get('access_token')

    with freeze_time('2021-01-01 12:31:00'):
        response = client.post(
            '/auth/refresh_token/',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}

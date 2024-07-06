from http import HTTPStatus

DEFAULT_PATH = '/auth'


def test_token(client, user):
    response = client.post(
        DEFAULT_PATH + '/token/',
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
        DEFAULT_PATH + '/token/',
        data={
            'username': 'email',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token__incorrect_password(client, user):
    response = client.post(
        DEFAULT_PATH + '/token/',
        data={
            'username': user.email,
            'password': user.password,  # Here we are using the hashed pwd
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}

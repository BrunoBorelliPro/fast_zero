from http import HTTPStatus


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


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'email': 'email@email.com',
                'id': 1,
                'username': 'username',
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'email': 'email@email.com',
            'username': 'username',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'email': 'email@email.com',
        'username': 'username',
        'id': 1,
    }
    assert response.json().get('password') is None


def test_update_user__user_not_found(client):
    response = client.put(
        '/users/2',
        json={
            'email': 'email@email.com',
            'username': 'username',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user__user_id_less_than_1(client):
    response = client.put(
        '/users/0',
        json={
            'email': 'email@email.com',
            'username': 'username',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user__user_not_found(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}

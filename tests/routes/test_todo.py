from http import HTTPStatus

from sqlalchemy import select

from fast_zero.models import Todo
from tests.conftest import TodoFactory


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        json={
            'title': 'title',
            'description': 'description',
            'state': 'todo',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json().get('title') == 'title'
    assert response.json().get('description') == 'description'
    assert response.json().get('state') == 'todo'
    assert response.json().get('updated_at') is not None
    assert response.json().get('created_at') is not None


def test_read_todos_should_return_5_todos(session, client, token, user):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(expected_todos, user_id=user.id)
    )
    session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_read_todos_should_return_15_todo(session, client, token, user):
    expected_todos = 15
    session.bulk_save_objects(
        TodoFactory.create_batch(expected_todos * 2, user_id=user.id)
    )
    session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        params={'limit': expected_todos},
    )

    assert len(response.json()['todos']) == expected_todos


def test_read_todos_filter_by_title(session, client, token, user):
    expected_todos = 5
    title = 'title'
    title2 = 'word'
    session.bulk_save_objects(
        TodoFactory.create_batch(expected_todos, user_id=user.id, title=title)
    )
    session.bulk_save_objects(
        TodoFactory.create_batch(expected_todos, user_id=user.id, title=title2)
    )
    session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        params={'title': title},
    )

    assert len(response.json()['todos']) == expected_todos


def test_read_todos_filter_by_description(session, client, token, user):
    expected_todos = 5
    description = 'description'
    description2 = 'word'
    session.bulk_save_objects(
        TodoFactory.create_batch(
            expected_todos, user_id=user.id, description=description
        )
    )
    session.bulk_save_objects(
        TodoFactory.create_batch(
            expected_todos, user_id=user.id, description=description2
        )
    )
    session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        params={'description': description},
    )

    assert len(response.json()['todos']) == expected_todos


def test_read_todos_filter_by_state(session, client, token, user):
    expected_todos = 5
    state = 'todo'
    state2 = 'done'
    session.bulk_save_objects(
        TodoFactory.create_batch(expected_todos, user_id=user.id, state=state)
    )
    session.bulk_save_objects(
        TodoFactory.create_batch(expected_todos, user_id=user.id, state=state2)
    )
    session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        params={'state': state},
    )

    assert len(response.json()['todos']) == expected_todos


def test_read_todos_filter_by_title_and_description(
    session, client, token, user
):
    expected_todos = 5
    title = 'title'
    description = 'description'
    title2 = 'word'
    description2 = 'word'
    session.bulk_save_objects(
        TodoFactory.create_batch(
            expected_todos,
            user_id=user.id,
            title=title,
            description=description,
        )
    )
    session.bulk_save_objects(
        TodoFactory.create_batch(
            expected_todos,
            user_id=user.id,
            title=title2,
            description=description2,
        )
    )
    session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        # filtragem cruzada
        params={'title': title, 'description': description},
    )

    assert len(response.json()['todos']) == expected_todos


def test_read_todos_filter_by_title_and_description_negative(
    session, client, token, user
):
    expected_todos = 5
    title = 'title'
    description = 'description'
    title2 = 'word'
    description2 = 'word'
    session.bulk_save_objects(
        TodoFactory.create_batch(
            expected_todos,
            user_id=user.id,
            title=title,
            description=description,
        )
    )
    session.bulk_save_objects(
        TodoFactory.create_batch(
            expected_todos,
            user_id=user.id,
            title=title2,
            description=description2,
        )
    )
    session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        # filtragem cruzada
        params={'title': title, 'description': description2},
    )

    assert len(response.json()['todos']) == 0


def test_read_todos_filter_by_title_and_state(session, client, token, user):
    expected_todos = 5
    title = 'title'
    state = 'todo'
    title2 = 'word'
    state2 = 'done'
    session.bulk_save_objects(
        TodoFactory.create_batch(
            expected_todos,
            user_id=user.id,
            title=title,
            state=state,
        )
    )
    session.bulk_save_objects(
        TodoFactory.create_batch(
            expected_todos,
            user_id=user.id,
            title=title2,
            state=state2,
        )
    )
    session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        params={'title': title, 'state': state},
    )

    assert len(response.json()['todos']) == expected_todos


def test_read_todos_filter_by_title_and_state_negative(
    session, client, token, user
):
    expected_todos = 5
    title = 'title'
    state = 'todo'
    title2 = 'word'
    state2 = 'done'
    session.bulk_save_objects(
        TodoFactory.create_batch(
            expected_todos,
            user_id=user.id,
            title=title,
            state=state,
        )
    )
    session.bulk_save_objects(
        TodoFactory.create_batch(
            expected_todos,
            user_id=user.id,
            title=title2,
            state=state2,
        )
    )
    session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        # filtragem cruzada
        params={'title': title, 'state': state2},
    )

    assert len(response.json()['todos']) == 0


def test_read_todos_filter_by_description_and_state(
    session, client, token, user
):
    expected_todos = 5
    description = 'description'
    state = 'todo'
    description2 = 'word'
    state2 = 'done'
    session.bulk_save_objects(
        TodoFactory.create_batch(
            expected_todos,
            user_id=user.id,
            description=description,
            state=state,
        )
    )
    session.bulk_save_objects(
        TodoFactory.create_batch(
            expected_todos,
            user_id=user.id,
            description=description2,
            state=state2,
        )
    )
    session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        params={'description': description, 'state': state},
    )

    assert len(response.json()['todos']) == expected_todos


def test_read_todos_filter_by_description_and_state_negative(
    session, client, token, user
):
    expected_todos = 5
    description = 'description'
    state = 'todo'
    description2 = 'word'
    state2 = 'done'
    session.bulk_save_objects(
        TodoFactory.create_batch(
            expected_todos,
            user_id=user.id,
            description=description,
            state=state,
        )
    )
    session.bulk_save_objects(
        TodoFactory.create_batch(
            expected_todos,
            user_id=user.id,
            description=description2,
            state=state2,
        )
    )
    session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        # filtragem cruzada
        params={'description': description, 'state': state2},
    )

    assert len(response.json()['todos']) == 0


def test_delete_todo_should_delete(session, client, token, user):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()

    response = client.delete(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Task has been deleted successfully.',
    }
    assert (
        session.scalar(
            select(Todo).where(Todo.user_id == user.id, Todo.id == todo.id)
        )
        is None
    )


def test_delete_todo_should_return_not_found(session, client, token, user):
    response = client.delete(
        '/todos/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


def test_delete_todo_should_return_unauthorized(session, client):
    response = client.delete('/todos/1')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_todo_update(session, client, token, todo):
    response = client.patch(
        f'/todos/{todo.id}',
        json={
            'title': 'new title',
            'description': 'new description',
            'state': 'doing',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json().get('title') == 'new title'
    assert response.json().get('description') == 'new description'
    assert response.json().get('state') == 'doing'
    assert response.json().get('id') == todo.id


def test_todo_should_update_only_title(session, client, token, todo):
    response = client.patch(
        f'/todos/{todo.id}',
        json={
            'title': 'new title',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json().get('title') == 'new title'
    assert response.json().get('description') == todo.description
    assert response.json().get('state') == todo.state
    assert response.json().get('id') == todo.id


def test_todo_should_update_only_description(session, client, token, todo):
    response = client.patch(
        f'/todos/{todo.id}',
        json={
            'description': 'new description',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json().get('title') == todo.title
    assert response.json().get('description') == 'new description'
    assert response.json().get('state') == todo.state
    assert response.json().get('id') == todo.id


def test_todo_should_update_only_state(session, client, token, todo):
    response = client.patch(
        f'/todos/{todo.id}',
        json={
            'state': 'doing',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json().get('title') == todo.title
    assert response.json().get('description') == todo.description
    assert response.json().get('state') == 'doing'
    assert response.json().get('id') == todo.id


def test_todo_update_should_no_update(session, client, token, todo):
    response = client.patch(
        f'/todos/{todo.id}',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json().get('title') == todo.title
    assert response.json().get('description') == todo.description
    assert response.json().get('state') == todo.state
    assert response.json().get('id') == todo.id


def test_todo_should_update_only_title_and_description(
    session, client, token, todo
):
    response = client.patch(
        f'/todos/{todo.id}',
        json={
            'title': 'new title',
            'description': 'new description',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json().get('title') == 'new title'
    assert response.json().get('description') == 'new description'
    assert response.json().get('state') == todo.state
    assert response.json().get('id') == todo.id


def test_todo_should_update_only_title_and_state(session, client, token, todo):
    response = client.patch(
        f'/todos/{todo.id}',
        json={
            'title': 'new title',
            'state': 'doing',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json().get('title') == 'new title'
    assert response.json().get('description') == todo.description
    assert response.json().get('state') == 'doing'
    assert response.json().get('id') == todo.id


def test_todo_should_update_only_description_and_state(
    session, client, token, todo
):
    response = client.patch(
        f'/todos/{todo.id}',
        json={
            'description': 'new description',
            'state': 'doing',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json().get('title') == todo.title
    assert response.json().get('description') == 'new description'
    assert response.json().get('state') == 'doing'
    assert response.json().get('id') == todo.id


def test_todo_update_should_return_not_found(session, client, token):
    response = client.patch(
        '/todos/1',
        json={
            'title': 'new title',
            'description': 'new description',
            'state': 'doing',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


def test_todo_update_should_return_unauthorized(session, client):
    response = client.patch(
        '/todos/1',
        json={
            'title': 'new title',
            'description': 'new description',
            'state': 'doing',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_todo_update_should_return_not_found_for_other_user_todo(
    session, client, token, other_user
):
    todo = TodoFactory(user_id=other_user.id)
    session.add(todo)
    session.commit()

    response = client.patch(
        f'/todos/{todo.id}',
        json={
            'title': 'new title',
            'description': 'new description',
            'state': 'doing',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}

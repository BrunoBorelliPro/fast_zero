import factory
import factory.fuzzy
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import Todo, TodoState, User, table_registry
from fast_zero.security import get_password_hash


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'User{n}_')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@teste.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@senha')


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture()
def session(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    pwd = 'testpassword'

    user = UserFactory(
        password=get_password_hash(pwd),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd

    return user


@pytest.fixture()
def other_user(session):
    pwd = 'testpassword2'

    user = UserFactory(
        password=get_password_hash('testpassword2'),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd
    return user


@pytest.fixture()
def token(client, user):
    response = client.post(
        '/auth/token/',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )

    return response.json().get('access_token')


@pytest.fixture()
def todo(session, user):
    todo = TodoFactory(user_id=user.id, state=TodoState.todo)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo

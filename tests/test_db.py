from time import sleep

from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(username='Bruno', password='senha123', email='bruno@email.com')
    session.add(user)
    session.commit()
    result = session.scalar(
        select(User).where(User.email == 'bruno@email.com')
    )

    assert result.id == 1


def test_update_user(session):
    user = User(username='Bruno', password='senha123', email='bruno@email.com')
    session.add(user)
    session.commit()

    sleep(1)

    user = session.scalar(select(User).where(User.id == 1))
    user.username = 'Bruno Borelli'
    session.commit()

    result = session.scalar(select(User).where(User.id == 1))

    assert result.username == 'Bruno Borelli'
    assert result.created_at < result.updated_at

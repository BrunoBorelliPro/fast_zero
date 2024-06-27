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

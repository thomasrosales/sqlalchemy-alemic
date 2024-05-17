from sqlalchemy import select

from .config import Session
from .models import Address, User


def create_user(name, last_name, emails):
    with Session() as session:
        addresses = [Address(email_address=email) for email in emails]
        user = User(
            name=name,
            fullname=f"{name} {last_name}",
            addresses=addresses,
        )
        session.add(user)
        session.commit()
        return user


def get_user_by_id(user_id):
    with Session() as session:
        stmp = select(User).where(User.id == user_id)
        return session.scalars(stmp).one_or_none()


def get_all_users():
    with Session() as session:
        stmp = select(User).order_by(User.id)
        return session.scalars(stmp).all()

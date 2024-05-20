from typing import List

from sqlalchemy import select, or_, func, update, insert, bindparam
from sqlalchemy.orm import aliased

from .config import Session
from .models import Address, User, Order, Product, OrderProduct


def create_user(name: str, last_name: str, emails: List[str], referrer_id: int) -> User:
    with Session() as session:
        addresses = [Address(email_address=email) for email in emails]
        user = User(
            name=name,
            fullname=f"{name} {last_name}",
            addresses=addresses,
            referrer_id=referrer_id,
        )
        session.add(user)
        session.commit()
        return user


def add_order(user_id: int) -> Order:
    with Session() as session:
        order = Order(user_id=user_id)
        session.add(order)
        session.commit()
        return order


def add_product(title: str, description: str) -> Product:
    with Session() as session:
        product = Product(
            title=title,
            description=description,
        )
        session.add(product)
        session.commit()
        return product


def add_product_to_order(order_id: int, product_id: int, quantity: int):
    with Session() as session:
        order_product = OrderProduct(
            quantity=quantity, order_id=order_id, product_id=product_id
        )
        session.add(order_product)
        session.commit()


def set_new_referrer(user_id: int, referrer_id: int):
    with Session() as session:
        stmp = (
            update(User)
            .where(User.id == user_id)
            .values(referrer_id=referrer_id)
        )
        result = session.execute(stmp)
        session.commit()
        return result


def bulk_insert_products_into_order_id(order_id: int, products: List[dict]):
    with Session() as session:
        stmp = (
            insert(OrderProduct)
            .values(
                order_id=order_id,
                product_id=bindparam("product_id"),
                quantity=bindparam("quantity")
            )
        )
        result = session.execute(stmp, products)
        session.commit()
        return result


def get_user_by_id(user_id):
    with Session() as session:
        stmp = select(User).where(User.id == user_id)
        return session.scalars(stmp).one_or_none()


def get_all_users():
    with Session() as session:
        # stmp_or = or_(User.name == user_name, User.id > user_id_range) if user_name else None
        # stmp_ilike =  User.name.ilike(f"%{user_name}%") if user_name else None
        stmp = select(User).order_by(User.created_at.asc()).limit(10)
        return session.scalars(stmp).all()


def get_user_name(user_id: int) -> str:
    with Session() as session:
        stmp = select(User.name).where(User.id == user_id)
        return session.scalars(stmp)


def select_all_invited_users():
    with Session() as session:
        ParentUser = aliased(User)
        ReferralUser = aliased(User)

        stmp = select(
            ParentUser.fullname.label("parent_name"),
            ReferralUser.fullname.label("referral_name"),
        ).join(
            ReferralUser, ReferralUser.referrer_id == ParentUser.id
        )  # outerjoin()
        return session.execute(stmp).all()


def select_all_user_orders(user_id: int):
    with Session() as session:
        stmp = (
            select(Product, Order, User.name, OrderProduct.quantity)
            .join(User.orders)
            .join(Order.order_products)
            .join(Product)
            .where(User.id == user_id)
        )
        return session.execute(stmp).all()


def get_total_number_of_orders():
    with Session() as session:
        stmp = (
            select(func.count(Order.id).label("total_orders"), User.fullname)
            .join(
                User
            )
            .group_by(User.id)
        )
        return session.execute(stmp).all()


def get_total_number_order_filter_by(min_amount: int = 0):
    with Session() as session:
        stmp = (
            select(func.sum(OrderProduct.quantity).label("quantity"), User.fullname)
            .join(Order, OrderProduct.order_id == Order.id)
            .join(
                User
            )
            .group_by(User.id)
            .having(func.sum(OrderProduct.quantity) > min_amount)
        )
        return session.execute(stmp).all()

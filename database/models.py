from typing import List, Optional

from sqlalchemy import DECIMAL, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import CommonMixin, TimeStampMixin


class User(Base, CommonMixin, TimeStampMixin):
    __tablename__ = "user_account"
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    # Relations

    referrer_id: Mapped[int] = mapped_column(
        ForeignKey("user_account.id", ondelete="SET NULL"), nullable=True
    )
    referrer: Mapped["User"] = relationship(
        backref="referrer_user", remote_side="User.id"
    )
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    orders: Mapped[List["Order"]] = relationship(
        back_populates="user", cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base, CommonMixin, TimeStampMixin):
    __tablename__ = "address"
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


class Product(Base, CommonMixin, TimeStampMixin):
    __tablename__ = "products"
    title: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(Text())

    # Relations

    order_products: Mapped[List["OrderProduct"]] = relationship(
        back_populates="product", cascade="all, delete"
    )


class Order(Base, CommonMixin, TimeStampMixin):
    __tablename__ = "orders"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_account.id", ondelete="SET NULL")
    )
    user: Mapped["User"] = relationship(back_populates="orders")

    order_products: Mapped[List["OrderProduct"]] = relationship(
        back_populates="order", cascade="all, delete"
    )


class OrderProduct(Base, CommonMixin):
    __tablename__ = "order_product"

    quantity: Mapped[float] = mapped_column(DECIMAL(precision=16, scale=4))

    # Relations

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT")
    )
    product: Mapped["Product"] = relationship(back_populates="order_products")

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    order: Mapped["Order"] = relationship(back_populates="order_products")

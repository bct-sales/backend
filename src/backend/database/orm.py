from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String



class Base(DeclarativeBase):
    pass


class SaleEvent(Base):
    __tablename__ = 'sale_events'

    sale_event_id: Mapped[int] = mapped_column(primary_key=True)

    date: Mapped[str] = mapped_column(String)

    description: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f'SaleEvent(sale_event_id={self.sale_event_id!r}, date={self.date!r}, description={self.description!r})'


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True)

    email_address: Mapped[str] = mapped_column(String)

    password_hash: Mapped[str] = mapped_column(String)

    items: Mapped[list[Item]] = relationship("Item", back_populates='owner')

    def __repr__(self) -> str:
        return f'User(user_id={self.user_id!r}, email_address={self.email_address!r}, password_hash={self.password_hash!r})'


class Item(Base):
    __tablename__ = 'items'

    item_id: Mapped[int] = mapped_column(primary_key=True)

    description: Mapped[str] = mapped_column(String)

    price_in_cents: Mapped[int] = mapped_column(Integer)

    owner: Mapped[User] = relationship("User", back_populates='items')

    recipient: Mapped[User] = relationship("User")

    sale_event: Mapped[SaleEvent] = relationship("SaleEvent")

    def __repr__(self) -> str:
        return f'Item(item_id={self.item_id!r}, description={self.description!r}, price_in_cents={self.price_in_cents!r})'


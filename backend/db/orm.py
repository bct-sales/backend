from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Date, Time, Boolean
from datetime import date, time


class Base(DeclarativeBase):
    pass


class SalesEvent(Base):
    __tablename__ = 'sales_events'

    sales_event_id: Mapped[int] = mapped_column(primary_key=True)

    date: Mapped[date] = mapped_column(Date)

    start_time: Mapped[time] = mapped_column(Time)

    end_time: Mapped[time] = mapped_column(Time)

    location: Mapped[str] = mapped_column(String)

    description: Mapped[str] = mapped_column(String)

    available: Mapped[bool] = mapped_column(Boolean)

    def __repr__(self) -> str:
        return f'SalesEvent(sales_event_id={self.sales_event_id!r}, date={self.date!r}, description={self.description!r}, available={self.available!r})'


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True)

    role: Mapped[str] = mapped_column(String)

    password_hash: Mapped[str] = mapped_column(String)

    items: Mapped[list[Item]] = relationship("Item", back_populates='owner', foreign_keys='Item.owner_id')

    def __repr__(self) -> str:
        return f'User(user_id={self.user_id!r}, role={self.role}, password_hash={self.password_hash!r})'


class Item(Base):
    __tablename__ = 'items'

    item_id: Mapped[int] = mapped_column(primary_key=True)

    description: Mapped[str] = mapped_column(String)

    category: Mapped[str] = mapped_column(String)

    price_in_cents: Mapped[int] = mapped_column(Integer)

    owner_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))

    owner: Mapped[User] = relationship("User", back_populates='items', foreign_keys=[owner_id])

    recipient_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))

    recipient: Mapped[User] = relationship("User", foreign_keys=[recipient_id])

    sales_event_id: Mapped[int] = mapped_column(ForeignKey('sales_events.sales_event_id'))

    sales_event: Mapped[SalesEvent] = relationship("SalesEvent", foreign_keys=[sales_event_id])

    charity: Mapped[bool] = mapped_column(Boolean)

    def __repr__(self) -> str:
        return f'Item(item_id={self.item_id!r}, description={self.description!r}, price_in_cents={self.price_in_cents!r})'


class Sale(Base):
    __tablename__ = 'sales'

    sale_id: Mapped[int] = mapped_column(primary_key=True)

    items_sold: Mapped[list[SaleItem]] = relationship("SaleItem", back_populates='sale', foreign_keys='SaleItem.sale_id')


class SaleItem(Base):
    __tablename__ = 'sale_items'

    sale_id: Mapped[int] = mapped_column(ForeignKey('sales.sale_id'), primary_key=True)

    item_id: Mapped[int] = mapped_column(ForeignKey('items.item_id'), primary_key=True)

    sale = relationship("Sale", foreign_keys=[sale_id])

    item_sold = relationship("Item", foreign_keys=[item_id])

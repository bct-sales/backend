from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint



class Base(DeclarativeBase):
    pass


class SalesEvent(Base):
    __tablename__ = 'sale_events'

    sale_event_id: Mapped[int] = mapped_column(primary_key=True)

    date: Mapped[str] = mapped_column(String)

    description: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f'SaleEvent(sale_event_id={self.sale_event_id!r}, date={self.date!r}, description={self.description!r})'


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True)

    role: Mapped[str] = mapped_column(String)

    email_address: Mapped[str] = mapped_column(String)

    password_hash: Mapped[str] = mapped_column(String)

    items: Mapped[list[Item]] = relationship("Item", back_populates='owner', foreign_keys='Item.owner_id')

    def __repr__(self) -> str:
        return f'User(user_id={self.user_id!r}, role={self.role}, email_address={self.email_address!r}, password_hash={self.password_hash!r})'

    __table_args__ = (
        UniqueConstraint('email_address'),
    )


class Item(Base):
    __tablename__ = 'items'

    item_id: Mapped[int] = mapped_column(primary_key=True)

    description: Mapped[str] = mapped_column(String)

    price_in_cents: Mapped[int] = mapped_column(Integer)

    owner_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))

    owner: Mapped[User] = relationship("User", back_populates='items', foreign_keys=[owner_id])

    recipient_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))

    recipient: Mapped[User] = relationship("User", foreign_keys=[recipient_id])

    sale_event_id: Mapped[int] = mapped_column(ForeignKey('sale_events.sale_event_id'))

    sale_event: Mapped[SalesEvent] = relationship("SaleEvent", foreign_keys=[sale_event_id])

    def __repr__(self) -> str:
        return f'Item(item_id={self.item_id!r}, description={self.description!r}, price_in_cents={self.price_in_cents!r})'


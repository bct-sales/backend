from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(String())
    password_hash: Mapped[str] = mapped_column(String())

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, email_address={self.email_address!r}, password_hash={self.password_hash!r})'

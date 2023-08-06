from contextlib import contextmanager
from typing import Callable, Optional, Type

from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import Pool

import backend.db.models as models
import backend.db.orm as orm
import backend.security as security
from backend.db.exceptions import *
from backend.security import roles

import logging


class DatabaseSession:
    __session: Session

    def __init__(self, session: Session):
        self.__session = session

    def close(self):
        self.__session.close()

    def create_user(self, user: models.UserCreate) -> None:
        if not security.is_valid_email_address(user.email_address):
            raise InvalidEmailAddressException
        if not security.is_valid_password(user.password):
            raise InvalidPasswordException
        if self.user_with_email_address_exists(email_address=user.email_address):
            raise EmailAddressAlreadyInUseException

        password_hash = security.hash_password(user.password)
        orm_user = orm.User(
            email_address=user.email_address,
            password_hash=password_hash,
            role=roles.SELLER.name,
        )
        try:
            self.__session.add(orm_user)
            self.__session.commit()
        except IntegrityError as e:
            logging.error(e)
            raise

    def user_with_email_address_exists(self, *, email_address: str) -> bool:
        return self.find_user_with_email_address(email_address=email_address) is not None

    def find_user_with_email_address(self, *, email_address: str) -> Optional[orm.User]:
        return self.__session.query(orm.User).filter(orm.User.email_address == email_address).first()

    def login(self, *, email_address: str, password: str) -> orm.User:
        user = self.find_user_with_email_address(email_address=email_address)
        if user is None:
            raise UnknownUserException
        if not security.verify_password(hash=user.password_hash, plaintext=password):
            raise WrongPasswordException
        return user

    def list_users(self) -> list[orm.User]:
        return self.__session.query(orm.User).all()

    def add_item(self, item: models.ItemCreate):
        orm_item = orm.Item(
            description=item.description,
            price_in_cents=item.price_in_cents,
            owner_id=item.owner_id,
            recipient_id=item.recipient_id,
            sale_event_id=item.sale_event_id,
        )
        self.__session.add(orm_item)
        self.__session.commit()

    def create_sales_event(self, sales_event: models.SalesEventCreate) -> int:
        if sales_event.start_time > sales_event.end_time:
            raise InvalidEventTimeInterval
        orm_sales_event = orm.SalesEvent(
            date=sales_event.date,
            start_time=sales_event.start_time,
            end_time=sales_event.end_time,
            location=sales_event.location,
            description=sales_event.description,
        )
        self.__session.add(orm_sales_event)
        self.__session.commit()
        return orm_sales_event.sale_event_id

    def find_sales_event_by_id(self, id: int) -> Optional[orm.SalesEvent]:
        return self.__session.query(orm.SalesEvent).filter(orm.SalesEvent.sale_event_id == id).first()

    def list_sales_events(self) -> list[orm.SalesEvent]:
        return self.__session.query(orm.SalesEvent).all()


class Database:
    __engine: Engine

    __session_maker: Callable[[], Session]

    def __init__(self, url, poolclass: Optional[Type[Pool]]=None):
        connect_args = {'check_same_thread': False}
        self.__engine = create_engine(url, connect_args=connect_args, poolclass=poolclass)
        self.__session_maker = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)

    def create_session(self) -> DatabaseSession:
        return DatabaseSession(self.__session_maker())

    @property
    @contextmanager
    def session(self):
        result = self.create_session()
        try:
            yield result
        finally:
            result.close()

    def drop_tables(self):
        orm.Base.metadata.drop_all(self.__engine)

    def create_tables(self):
        orm.Base.metadata.create_all(self.__engine)

    def dispose(self):
        self.__engine.dispose()

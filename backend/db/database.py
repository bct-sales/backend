from __future__ import annotations
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

import logging

from backend.security import roles


class Database:
    __name: str

    __engine: Engine

    __session_maker: Callable[[], Session]

    def __init__(self, name: str, url: str, poolclass: Optional[Type[Pool]]=None):
        self.__name = name
        connect_args = {'check_same_thread': False}
        self.__engine = create_engine(url, connect_args=connect_args, poolclass=poolclass)
        self.__session_maker = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)

    def create_session(self) -> DatabaseSession:
        return DatabaseSession(self, self.__session_maker())

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

    def __str__(self):
        return f'{self.__name}@{id(self):016x}'


class DatabaseSession:
    __session: Session

    __parent_database: Database

    __logger: logging.Logger

    def __init__(self, parent: Database, session: Session):
        self.__logger = logging.getLogger('database')
        self.__session = session
        self.__parent_database = parent

    def close(self):
        self.__session.close()

    def create_user_with_id(self, user_id: int, user: models.UserCreate) -> orm.User:
        self.__logger.debug(f'Creating user with id {user_id}')
        if not security.is_valid_password(user.password):
            raise InvalidPasswordException
        if not roles.is_valid_role(user.role):
            raise InvalidRoleException

        password_hash = security.hash_password(user.password)
        orm_user = orm.User(
            user_id=user_id,
            password_hash=password_hash,
            role=user.role,
        )
        try:
            self.__session.add(orm_user)
            self.__session.commit()
            return orm_user
        except IntegrityError as e:
            logging.error(e)
            raise

    def find_user_with_id(self, *, user_id: int) -> Optional[orm.User]:
        self.__logger.debug(f'Looking for user with id {user_id!r}')
        return self.__session.query(orm.User).filter(orm.User.user_id == user_id).first()

    def login_with_id(self, *, user_id: int, password: str) -> orm.User:
        self.__logger.debug(f'Checking password for user with id {user_id!r}')
        user = self.find_user_with_id(user_id=user_id)
        if user is None:
            raise UnknownUserException
        if not security.verify_password(hash=user.password_hash, plaintext=password):
            raise WrongPasswordException
        return user

    def list_users(self) -> list[orm.User]:
        return self.__session.query(orm.User).all()

    def create_item(self, *, item: models.ItemCreate) -> orm.Item:
        self.__logger.debug(f'Creating item with data {item!r}')
        orm_item = orm.Item(
            description=item.description,
            category=item.category,
            price_in_cents=item.price_in_cents,
            owner_id=item.owner_id,
            recipient_id=item.recipient_id,
            sales_event_id=item.sales_event_id,
            charity=item.charity,
        )
        self.__session.add(orm_item)
        self.__session.commit()
        return orm_item

    def list_items_owned_by(self, *, owner: int, sale_event: int) -> list[orm.Item]:
        self.__logger.debug(f'Looking for items created by user {owner!r}')
        return self.__session.query(orm.Item).filter(orm.Item.owner_id == owner).filter(orm.Item.sales_event_id == sale_event).all()

    def list_items(self) -> list[orm.Item]:
        self.__logger.debug(f'Looking for all items')
        return self.__session.query(orm.Item).all()

    def list_sales(self) -> list[orm.Sale]:
        return self.__session.query(orm.Sale).all()

    def create_sales_event(self, sales_event: models.SalesEventCreate) -> orm.SalesEvent:
        self.__logger.debug(f'Creating sales event with data {sales_event!r}')
        if sales_event.start_time > sales_event.end_time:
            raise InvalidEventTimeInterval
        orm_sales_event = orm.SalesEvent(
            date=sales_event.date,
            start_time=sales_event.start_time,
            end_time=sales_event.end_time,
            location=sales_event.location,
            description=sales_event.description,
            available=sales_event.available,
        )
        self.__session.add(orm_sales_event)
        self.__session.commit()
        return orm_sales_event

    def find_sales_event_by_id(self, id: int) -> Optional[orm.SalesEvent]:
        self.__logger.debug(f'Looking for sale event with id {id!r}')
        return self.__session.query(orm.SalesEvent).filter(orm.SalesEvent.sales_event_id == id).first()

    def list_sales_events(self) -> list[orm.SalesEvent]:
        self.__logger.debug(f'Listing all events')
        return self.__session.query(orm.SalesEvent).all()

    def find_item_by_id(self, id: int) -> Optional[orm.Item]:
        self.__logger.debug(f'Finding item with id {id!r}')
        return self.__session.query(orm.Item).filter(orm.Item.item_id == id).first()

    def item_with_id_exists(self, id: int) -> bool:
        return self.find_item_by_id(id) is not None

    def delete_item_by_id(self, id: int) -> None:
        delete_count = self.__session.query(orm.Item).filter(orm.Item.item_id == id).delete()
        self.__session.commit()
        logging.info(f'Deleted {delete_count} item(s)')

    def update_event(self, *, id: int, **kwargs) -> None:
        orm_sales_event = self.find_sales_event_by_id(id)
        if orm_sales_event is None:
            raise UnknownSalesEventException
        for field, value in kwargs.items():
            if value is not None:
                setattr(orm_sales_event, field, value)
        self.__session.commit()

    def update_item(self, *, item_id: int, owner_id: int, **kwargs) -> None:
        orm_item = self.find_item_by_id(id=item_id)
        if orm_item is None:
            raise UnknownItemException
        if orm_item.owner_id != owner_id:
            raise UnauthorizedItemChangeException
        for field, value in kwargs.items():
            if value is not None:
                setattr(orm_item, field, value)
        self.__session.commit()

    def has_item_been_sold(self, item_id: int) -> bool:
        return bool(self.__session.query(orm.SaleItem).filter(orm.SaleItem.item_id == item_id).first())

    def collect_sold_items(self) -> list[int]:
        return [row[0] for row in self.__session.query(orm.SaleItem.item_id).all()]

    def create_sale(self, item_ids: list[int]) -> orm.Sale:
        if len(item_ids) == 0:
            logging.error('Empty sale rejected')
            raise EmptySaleIsInvalid()
        if not all(self.item_with_id_exists(id) for id in item_ids):
            logging.error('Unknown item in sale')
            raise UnknownItemException()
        sale = orm.Sale()
        self.__session.add(sale)
        self.__session.commit()
        try:
            sale_items = [
                orm.SaleItem(
                    sale_id=sale.sale_id,
                    item_id=item_id
                )
                for item_id in item_ids
            ]
            self.__session.add_all(sale_items)
            self.__session.commit()
            return sale
        except IntegrityError:
            logging.error('Integrity error; assuming this is due to duplicate items')
            raise DuplicateItemsInSale()

    def commit(self) -> None:
        self.__session.commit()

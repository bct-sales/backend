from contextlib import contextmanager
from typing import Callable, Optional, Type

from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import Pool

import backend.database.models as models
import backend.database.orm as orm
import backend.security as security
from backend.database.exceptions import *


class DatabaseSession:
    __session: Session

    def __init__(self, session: Session):
        self.__session = session

    def close(self):
        self.__session.close()

    def create_user(self, user: models.UserCreate) -> None:
        if not security.is_valid_password(user.password):
            raise InvalidPasswordException()
        password_hash = security.hash_password(user.password)
        orm_user = orm.User(
            email_address=user.email_address,
            password_hash=password_hash,
            role=user.role,
        )
        try:
            self.__session.add(orm_user)
            self.__session.commit()
        except IntegrityError as e:
            raise EmailAddressAlreadyInUseException from e

    def find_user_with_email_address(self, *, email_address: str) -> Optional[orm.User]:
        return self.__session.query(orm.User).filter(orm.User.email_address == email_address).first()

    def login(self, *, email_address: str, password: str) -> Optional[orm.User]:
        if user := self.find_user_with_email_address(email_address=email_address):
            if security.verify_password(hash=user.password_hash, plaintext=password):
                return user

    def list_users(self) -> list[orm.User]:
        return self.__session.query(orm.User).all()

    def list_items(self) -> list[models.Item]:
        return []

    def begin(self) -> None:
        self.__session.begin()

    def commit(self) -> None:
        self.__session.commit()


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

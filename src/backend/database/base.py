import backend.database.models as models
import backend.database.orm as orm
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Callable



class DatabaseSession:
    __session: Session

    def __init__(self, session: Session):
        self.__session = session

    def close(self):
        self.__session.close()

    def list_users(self) -> list[models.User]:
        return []

    def list_items(self) -> list[models.Item]:
        return [
            models.Item(description="tralala", price_in_cents=100, item_id=0)
        ]


class Database:
    __engine: Engine

    __session_maker: Callable[[], Session]

    def __init__(self, url):
        connect_args = {'check_same_thread': False}
        self.__engine = create_engine(url, connect_args=connect_args)
        self.__session_maker = sessionmaker(autocommit=False, autoflush=False, autobegin=False, bind=self.__engine)

    def create_session(self) -> DatabaseSession:
        return DatabaseSession(self.__session_maker())

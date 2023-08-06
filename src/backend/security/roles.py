from __future__ import annotations
from backend.security import scopes


class Role:
    __name: str

    __scopes: scopes.Scopes

    @staticmethod
    def from_name(name: str) -> Role:
        if name not in _roles:
            raise RoleException(f'Unknown role {name}')
        return _roles[name]

    def __init__(self, name: str, scopes: scopes.Scopes):
        self.__name = name
        self.__scopes = scopes

    @property
    def name(self) -> str:
        return self.__name

    @property
    def scopes(self) -> scopes.Scopes:
        return self.__scopes


class RoleException(Exception):
    pass


_roles: dict[str, Role] = {}


def define_role(name: str, scopes: scopes.Scopes) -> Role:
    role = Role(name=name, scopes=scopes)
    _roles[name] = role
    return role


SELLER = define_role('seller', scopes.Scopes(scopes.ADD_ITEM, scopes.LIST_OWN_ITEMS))

ADMIN = define_role('admin', scopes.Scopes(scopes.LIST_ACCOUNTS, scopes.LIST_ALL_ITEMS))

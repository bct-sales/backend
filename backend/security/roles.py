from __future__ import annotations
from typing import Literal, cast
from backend.security import scopes


RoleName = Literal['seller', 'admin', 'cashier']

class Role:
    __name: RoleName

    __scopes: scopes.Scopes

    @staticmethod
    def from_name(name: str) -> Role:
        if not name in _roles:
            raise RoleException(f'Unknown role {name}')
        return _roles[cast(RoleName, name)]

    def __init__(self, name: RoleName, scopes: scopes.Scopes):
        self.__name = name
        self.__scopes = scopes

    @property
    def name(self) -> RoleName:
        return self.__name

    @property
    def scopes(self) -> scopes.Scopes:
        return self.__scopes

    def __str__(self):
        return self.__name

    def __repr__(self):
        return f'roles.{self.__name}'


class RoleException(Exception):
    pass


_roles: dict[RoleName, Role] = {}


def define_role(name: RoleName, scopes: scopes.Scopes) -> Role:
    role = Role(name=name, scopes=scopes)
    _roles[name] = role
    return role


SELLER = define_role('seller', scopes.Scopes(
    scopes.ADD_OWN_ITEM,
    # scopes.EDIT_OWN_ITEM,
    # scopes.REMOVE_OWN_ITEM,
    scopes.LIST_OWN_ITEMS,
    scopes.LIST_SALES_EVENTS,
))

ADMIN = define_role('admin', scopes.Scopes(
    scopes.LIST_ACCOUNTS,
    scopes.LIST_ALL_ITEMS,
    scopes.LIST_SALES_EVENTS,
    scopes.LIST_UNAVAILABLE_SALES_EVENTS,
    scopes.ADD_SALES_EVENTS,
    scopes.EDIT_SALES_EVENT,
))

CASHIER = define_role('cashier', scopes.Scopes(
    scopes.GET_ITEM_DATA
))

from __future__ import annotations

from typing import Iterator


class Scope:
    def __init__(self, name: str, description: str):
        self.__name = name
        self.__description = description

    @staticmethod
    def from_name(name: str) -> Scope:
        if name not in _scopes:
            raise ScopeException(f'No scope with name {name}')
        return _scopes[name]

    @property
    def name(self) -> str:
        return self.__name

    @property
    def description(self) -> str:
        return self.__description

    def __hash__(self) -> int:
        return hash(self.__name)

    def __str__(self) -> str:
        return self.__name

    def __repr__(self) -> str:
        return f'Scope(name={self.name!r}, description={self.description!r})'

class Scopes:
    __scopes: frozenset[Scope]

    def __init__(self, *scopes):
        self.__scopes = frozenset(scopes)

    @property
    def scopes(self) -> frozenset[Scope]:
        return self.__scopes

    def __iter__(self) -> Iterator[Scope]:
        return iter(self.__scopes)

    def has_permissions_for(self, scopes: Scopes) -> bool:
        return self.scopes >= scopes.scopes

    def __eq__(self, other) -> bool:
        if isinstance(other, Scopes):
            return self.scopes == other.scopes
        else:
            return NotImplemented

    def __str__(self):
        return " ".join(str(scope) for scope in self.__scopes)

    def __repr__(self):
        return f"Scopes({', '.join(repr(scope) for scope in self)})"


class ScopeException(Exception):
    pass


_scopes: dict[str, Scope] = {}


def define_scope(name: str, description: str):
    if name in _scopes:
        raise ScopeException('Cannot have two scopes with the same name')
    _scopes[name] = (scope := Scope(name, description))
    return scope


# Events
LIST_SALES_EVENTS = define_scope('events:list', 'List all sales events')
LIST_UNAVAILABLE_SALES_EVENTS = define_scope('events:list:unavailable', 'List unavailable sales events')
ADD_SALES_EVENTS = define_scope('events:add', 'Add sales events')
EDIT_SALES_EVENT = define_scope('events:edit', 'Edit sales events')

# Accounts
LIST_ACCOUNTS = define_scope('accounts:list', 'List all accounts')

# Items
GET_ITEM_DATA = define_scope('items:get', 'Get item data')
LIST_ALL_ITEMS = define_scope('items:list-all', 'List all items')
LIST_OWN_ITEMS = define_scope('items:list-own', 'List own items')
ADD_OWN_ITEM = define_scope('items:add-own', 'Add own item')
EDIT_OWN_ITEM = define_scope('items:edit-own', 'Edit own item')
REMOVE_OWN_ITEM = define_scope('items:remove-own', 'Remove own item')

# Sales
REGISTER_SALE = define_scope('sales:add', 'Register sale')


def all_scopes() -> set[Scope]:
    return set(_scopes.values())

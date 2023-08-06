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
ADD_SALES_EVENTS = define_scope('events:add', 'Add sales events')

# Accounts
LIST_ACCOUNTS = define_scope('accounts:list', 'List all accounts')

# Items
LIST_ALL_ITEMS = define_scope('items:list-all', 'List all items')
LIST_OWN_ITEMS = define_scope('items:list-own', 'List own items')
ADD_ITEM = define_scope('items:add', 'Add item')

def all_scopes() -> set[Scope]:
    return set(_scopes.values())

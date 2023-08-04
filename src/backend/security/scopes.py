from __future__ import annotations


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


class ScopeException(Exception):
    pass


_scopes: dict[str, Scope] = {}


def define_scope(name: str, description: str):
    if name in _scopes:
        raise ScopeException('Cannot have two scopes with the same name')
    _scopes[name] = (scope := Scope(name, description))
    return scope


LIST_ACCOUNTS = define_scope('accounts:list', 'List all accounts')


def all_scopes() -> set[Scope]:
    return set(_scopes.values())

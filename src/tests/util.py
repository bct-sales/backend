from typing import TypeVar


K = TypeVar('K')
V = TypeVar('V')


class Exists:
    def __eq__(self, other):
        return True

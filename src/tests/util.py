from typing import Any, TypeVar


K = TypeVar('K')
V = TypeVar('V')


class Exists:
    def __eq__(self, other: Any):
        return True

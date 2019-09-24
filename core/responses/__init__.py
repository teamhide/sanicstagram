from dataclasses import dataclass
from typing import Any


@dataclass
class ResponseSuccess:
    data: Any
    meta: Any

    def __bool__(self):
        return True


@dataclass
class ResponseFailure:
    data: Any
    meta: Any

    def __bool__(self):
        return False

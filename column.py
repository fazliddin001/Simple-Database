from typing import Optional, Any, Callable
from dataclasses import dataclass


@dataclass
class Col:
    title: str
    default_value: Optional[Any] | Callable = None
    index: Optional[int] = None

    def transform(self, value: Any = None) -> hash:
        if value is None and self.default_value is None:
            raise ValueError("Default value not found")

        elif value is None:
            if callable(self.default_value):
                val = self.default_value()
                return val
            else:
                return self.default_value

        else:
            return value

    def set_index(self, index):
        self.index = index

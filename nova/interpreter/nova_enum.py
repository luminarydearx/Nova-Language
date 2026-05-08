"""NovaEnum for Nova-Language2"""
from typing import List


class NovaEnum:
    """Represents a Nova enum"""
    def __init__(self, name: str, values: List[str]):
        self.name = name
        self.values = values
        # Create a dictionary-like object for the enum
        self.value_map = {v: v for v in values}

    def get_value(self, name: str):
        """Get enum value by name"""
        if name in self.value_map:
            return self.value_map[name]
        raise Exception(f"Enum '{self.name}' has no value '{name}'")

    def has_value(self, name: str) -> bool:
        """Check if enum has a value"""
        return name in self.value_map

    def __str__(self):
        return f"<enum {self.name}: {', '.join(self.values)}>"

    def __repr__(self):
        return f"NovaEnum({self.name})"
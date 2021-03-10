import enum
from extension import emoji


class Cards(enum.Enum):
    def _generate_next_value_(name, *_):
        name = name.capitalize() + "Card"
        return emoji(name)

    RED = enum.auto()
    BLUE = enum.auto()
    GREEN = enum.auto()
    YELLOW = enum.auto()
    WHITE = enum.auto()
    PINK = enum.auto()

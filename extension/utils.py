import enum
from extension import emoji


class Cards(enum.Enum):
    """
    Enumeração para as cartas do jogo.

    O valor de cada atributo corresponde ao seu emoji - veja Nota.

    Nota
    ----
    O valor do atributo é gerado pelo seu nome capitalizado e sufixado
    com `Card`, depois é pego o valor utilizando `extension.utils.emoji`
    """
    def _generate_next_value_(name, *_):
        name = name.capitalize() + "Card"
        return emoji(name)

    RED = enum.auto()
    BLUE = enum.auto()
    GREEN = enum.auto()
    YELLOW = enum.auto()
    WHITE = enum.auto()
    PINK = enum.auto()

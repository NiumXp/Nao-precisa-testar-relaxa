import os
import json
import enum
import __main__
import typing as t

# Pega o caminho todo para o arquivo principal.
_main_file_path = __main__.__file__
# Pega o caminho em que o arquivo principal está.
_main_path = os.path.dirname(_main_file_path)

def asset(*values):
    """
    Retorna o caminho para o asset baseado no arquivo principal.

    Parametros
    ----------
    *values : Tuple[str]
        Caminhos para o arquivo e o nome do arquivo.

    Retorno
    -------
    str
        Caminho para o arquivo.
    """
    return os.path.join(_main_path, "assets", *values)

# Pega o caminho para o JSON dos emojis.
_emojis_path = asset("emojis.json")
# Abre o arquivo para pegar o conteúdo.
with open(_emojis_path, encoding="utf-8") as _emojis:
    # Transforma o conteúdo em um dicionário.
    _emojis = json.load(_emojis)

def emoji(name: str) -> t.Optional[str]:
    """
    Retorna o emoji com nome `name` que estiver em assets/emojis.json.
    Retorna `None` se não encontrar.

    Parâmetros
    ----------
    name : str
        Nome do emoji.

    Retornos
    --------
    t.Optional[str]
        Retorna uma string se o emoji for encontrado, caso contrário, 
        retorna `None`.
    """
    return _emojis.get(name)


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

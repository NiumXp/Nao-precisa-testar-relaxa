import os
import json
import __main__
import typing as t

from .bot import CardBot

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

_emojis_path = asset("emojis.json")
with open(_emojis_path, encoding="utf-8") as _emojis:
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

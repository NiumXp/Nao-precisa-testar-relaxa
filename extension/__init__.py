import os
import __main__

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

import random

from extension.utils import Cards


class Player:
    """
    Atributos
    ---------
    lifes : list[Heart]
        Vidas do jogador.
    cards : list[utils.Cards]
        Cartas do jogador.
    """
    def __init__(self, user):
        self.user = user

        self.lifes = list()
        self.cards = self._random_cards()

    @staticmethod
    def _random_cards() -> list:
        return random.choices(list(Cards), k=10)

    @property
    def dead(self) -> bool:
        """Diz se o jogador está morto."""
        return bool(self.lifes)

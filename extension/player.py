import discord

import random
import collections

from extension import utils


class Player:
    """
    Atributos
    ---------
    lifes : list[Heart]
        Vidas do jogador.
    cards : list[utils.Cards]
        Cartas do jogador.
    """
    def __init__(self, user: discord.User):
        self.user = user

        self.lifes = list(utils.Hearts)
        self.cards = self._random_cards()

    @staticmethod
    def _random_cards() -> list:
        return random.choices(list(utils.Cards), k=10)

    def embed(self) -> discord.Embed:
        # cards = collections.Counter(self.cards)
        # cards = " ".join(f"{k.value}x{v}" for k, v in cards.items())
        cards = ''.join(l.value for l in self.cards)
        hearts = ' '.join(l.value for l in self.lifes)

        return discord.Embed(color=0xFFA500,
        ).set_thumbnail(url=self.user.avatar_url
        ).add_field(name="Corações", value=hearts, inline=False
        ).add_field(name="Cartas " + utils.emoji("Cards"), value=cards)

    @property
    def dead(self) -> bool:
        """Diz se o jogador está morto."""
        return not bool(self.lifes)

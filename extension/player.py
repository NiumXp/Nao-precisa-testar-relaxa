import discord

import random

from extension import utils


class Player:
    """
    Estrutura de um jogador para facíl manipulação com as cartas e
    corações dele.

    Parâmetros
    ----------
    user : discord.User
        Usuário do jogador.

    Atributos
    ---------
    user : discord.User
        Usuário do jogador.
    lifes : list[Heart]
        Vidas do jogador.
    cards : list[utils.Cards]
        Cartas do jogador.
    last_card : utils.Cards
        Última carta que o jogador jogou.
    """
    def __init__(self, user: discord.User):
        self.user = user

        # Cria o atributo de vida com todas os corações disponíveis. 
        self.lifes = list(utils.Hearts)
        # Cria o atributo de cartas só que com cartas aleatórias.
        self.cards = self._random_cards(5)

        # Cria o atributo da ultima carta jogada.
        self.last_card = None

    @staticmethod
    def _random_cards(amount) -> list:
        """Retorna uma lista com `amount` cartas aleatórias."""
        return random.choices(list(utils.Cards), k=amount)

    def embed(self) -> discord.Embed:
        """
        Retora um `discord.Embed` com os corações e cartas do jogador.
        """
        # Cria uma função que será a "chave" para uma ordenação.
        key = lambda i: i.value

        # Ordena as cartas para mostrar bonitinho.
        cards = sorted(self.cards, key=key)
        # Transforma a lista de cartas em uma string com todas elas
        # ordenadas e juntas.
        cards = ' '.join(l.value for l in cards)

        # Ordena todos os corações do jogador.
        hearts = sorted(self.lifes, key=key)
        # Transforma a lista de cartas em uma string com todas elas
        # ordenadas e juntas.
        hearts = ' '.join(l.value for l in self.lifes)

        # Ultima carta jogada.
        last_card = self.last_card.value if self.last_card else "Nenhuma"

        # Retorna um Embed com os fileds dos corações, última carta
        # jogada e cartas.
        return discord.Embed(color=0xFFA500,
        ).set_thumbnail(url=self.user.avatar_url
        ).add_field(name="Corações", value=hearts, inline=True
        ).add_field(name="Última carta", value=last_card
        ).add_field(name="Cartas " + utils.emoji("Cards"),
                    value=cards or "Nenhuma", inline=False)

    @property
    def dead(self) -> bool:
        """Diz se o jogador está morto."""
        return not bool(self.lifes)

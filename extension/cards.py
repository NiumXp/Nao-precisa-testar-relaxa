import random
import typing as t

from .utils import Hearts, Cards


class CardAction:
    async def execute(self, player, enemy) -> t.Tuple[str, str]:
        raise NotImplementedError()


class RemoveHeartAction(CardAction):
    """
    Remove o coração retornado de `get_heart` do oponente.
    """
    def get_heart(self) -> Hearts:
        raise NotImplementedError()

    async def execute(self, player, enemy) -> t.Tuple[str, str]:
        # Gera o coração para ser removido.
        heart = self.get_heart(enemy)

        # Verifica se o oponente tem o coração gerado.
        if heart in enemy.lifes:
            # Remove o coração do oponente.
            enemy.lifes.remove(heart)
        else:
            return f"Você tentou remover um coração {heart.value} do seu oponente!", f"O seu oponente tentou retirar um coração {heart.value} seu!"

        return f"Você removeu um coração {heart.value} do seu oponente!", f"O seu oponente retirou um coração {heart.value} seu!"


class Red(RemoveHeartAction):
    """
    O usuário remove o coração vermelho do seu openente.
    """
    def get_heart(self, _):
        return Hearts.RED


class Yellow(RemoveHeartAction):
    """
    O usuário remove o coração amarelo do seu openente.
    """
    def get_heart(self, _):
        return Hearts.YELLOW


class Green(RemoveHeartAction):
    """
    O usuário remove o coração verde do seu oponente.
    """
    def get_heart(self, _):
        return Hearts.GREEN


class Blue(RemoveHeartAction):
    """
    O usuário remove qualquer coração do seu oponente.
    """
    def get_heart(self, enemy):
        # Retorna um coração aleatório do inimigo.
        return random.choice(enemy.lifes)


class White(CardAction):
    """
    O usuário remove uma carta do seu oponente.

    Se o seu oponente não tiver nenhuma carta, a carta é perdida.
    """
    async def execute(self, player, enemy):
        items = len(enemy.cards)
        if items == 0:
            return "O seu inimigo não tinha cartas para serem removidas!", "O seu oponente tentou tirar uma carta sua!"

        random_index = random.randrange(items)
        card = enemy.cards.pop(random_index)

        return f"Você removeu uma carta {card.name} {card.value} do seu oponente!", f"O seu oponente removeu uma carta {card.name} {card.value} sua!"


class Black(CardAction):
    """
    O usuário recebe uma carta aleatória (não é possível receber uma
    carta preta). 
    """
    async def execute(self, player, enemy):
        cards = list(Cards)
        cards.remove(Cards.BLACK)

        card = random.choice(cards)
        player.cards.append(card)

        return f"Você recebeu uma carta {card.name} {card.value}!", f"O seu oponente recebeu uma carta {card.name} {card.value}!"


class Pink(CardAction):
    """
    Faz o usuário repetir o que a última carta jogada fez.

    Por exemplo, se o jogador jogou uma carta vermelha e em seguida
    jogou uma carta rosa, a carta rosa fará o que a carta vermelha fez.

    Se for a carta rosa for a primeira carta jogada, ela será perdida.
    """
    async def execute(self, player, enemy):
        last_card = player.last_card
        if not last_card:
            return "Você perdeu uma carta rosa!", "O seu oponente perdeu uma carta rosa!"
        card = get_by_name(last_card.name)
        return await card.execute(player, enemy)


class Orange(CardAction):
    """
    O usuário recebe um coração aleatório!
    """
    async def execute(self, player, enemy):
        hearts = list(Hearts)
        heart = random.choice(hearts)
        player.lifes.append(heart)
        return f"Você recebeu um coração {heart.value}!", f"O seu oponente recebeu um coração {heart.value}!"


# Todas as cartas.
all = [Red, Yellow, Green, Blue, White, Black, Pink, Orange]


def get_by_name(name: str):
    """
    Retorna a ação da carta que tiver o nome `name`. Retorna `None` se
    não existir.

    Parâmetros
    ----------
    name : str
        Nome da carta.

    Retorno
    -------
    typing.Type[CardAction]
        Ação da carta, pode ser `None`.
    """
    # Capitaliza `name`.
    name = name.capitalize()
    # Percorre todas as CardAction registradas.
    for card in all:
        # Se a classe tiver o mesmo que nome que `name`
        if card.__name__ == name:
            # retorna uma intância dela.
            return card()
    return None

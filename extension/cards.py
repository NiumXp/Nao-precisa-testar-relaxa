import random
import typing as t

from .utils import Hearts, Cards


class CardAction:
    async def execute(self, player, enemy) -> t.Tuple[str, str]:
        raise NotImplementedError()


class RemoveHeartAction(CardAction):
    def get_heart(self) -> Hearts:
        raise NotImplementedError()

    async def execute(self, player, enemy) -> t.Tuple[str, str]:
        heart = self.get_heart(enemy)

        if heart in enemy.lifes:
            enemy.lifes.remove(heart)
        else:
            return f"Você tentou remover um coração {heart.value} do seu oponente!", f"O seu oponente tentou retirar um coração {heart.value} seu!"

        return f"Você removeu um coração {heart.value} do seu oponente!", f"O seu oponente retirou um coração {heart.value} seu!"


class Red(RemoveHeartAction):
    def get_heart(self, _):
        return Hearts.RED


class Yellow(RemoveHeartAction):
    def get_heart(self, _):
        return Hearts.YELLOW


class Green(RemoveHeartAction):
    def get_heart(self, _):
        return Hearts.GREEN


class Blue(RemoveHeartAction):
    def get_heart(self, enemy):
        return random.choice(enemy.lifes)


class White(CardAction):
    async def execute(self, player, enemy):
        items = len(enemy.cards)
        if items == 0:
            return "O seu inimigo não tinha cartas para serem removidas!", "O seu oponente tentou tirar uma carta sua!"

        random_index = random.randrange(items)
        card = enemy.cards.pop(random_index)

        return f"Você removeu uma carta {card.name} {card.value} do seu oponente!", f"O seu oponente removeu uma carta {card.name} {card.value} sua!"


class Black(CardAction):
    async def execute(self, player, enemy):
        cards = list(Cards)
        cards.remove(Cards.BLACK)

        card = random.choice(cards)
        player.cards.append(card)

        return f"Você recebeu uma carta {card.name} {card.value}!", f"O seu oponente recebeu uma carta {card.name} {card.value}!"


class Pink(CardAction):
    async def execute(self, player, enemy):
        card = get_by_name(player.last_card.name)
        return await card.execute(player, enemy)


all = [Red, Yellow, Green, Blue, White, Black, Pink]


def get_by_name(name: str):
    # Percorre todas as CardAction registradas.
    for card in all:
        # Se a classe tiver o mesmo que nome que `name`
        if card.__name__ == name:
            # retorna uma intância dela.
            return card()
    return None

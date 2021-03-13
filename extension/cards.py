import random
import typing as t

from .utils import Hearts


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


all = [Red, Yellow, Green, Blue]


def get_by_name(name: str):
    # Percorre todas as CardAction registradas.
    for card in all:
        # Se a classe tiver o mesmo que nome que `name`
        if card.__name__ == name:
            # retorna uma intância dela.
            return card()
    return None

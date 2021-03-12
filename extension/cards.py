class CardAction:
    async def execute(self, player, enemy) -> str:
        raise NotImplementedError()

def get_by_name(name: str):
    # Percorre todas as subclasses de CardAction.
    for card in CardAction.__subclasses__():
        # Se a subclasse tiver o mesmo que nome que `name`
        if card.__name__ == name:
            # retorna uma intância dela.
            return card()
    return None

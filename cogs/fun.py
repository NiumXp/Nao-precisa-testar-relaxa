from discord.ext import commands
import discord

import asyncio
import typing as t

from extension import Player, cards
from extension.utils import Hearts, Cards


class Fun(commands.Cog):
    """
    Comandos de diversão!
    """
    def __init__(self, bot: t.Type[commands.Bot]):
        self.bot = bot

    async def get_turn_action(self, player: Player) -> t.Optional[Cards]:
        """
        Faz o turno do jogador e retorna a carta escolhida.

        Parâmetros
        ----------
        player : Player
            Jogador que terá seu turno feito.

        Raises
        ------
        discord.Forbidden
            Não foi possível enviar mensagem para o jogador.

        Retornos
        --------
        typing.Optional[Cards]
            Carta que o jogador selecionou, caso não selecionou nada,
            retorna `None`.
        """
        # Envia uma mensagem para o jogador dizendo que é a sua vez.
        message = await player.user.send(
            "É a sua vez! Escolha a sua carta!",
            embed=player.embed())

        # Adiciona o emoji das cartas que o jogador tiver.
        #
        # Nota: Transformar em `set` é para remover repetições e o BOT
        # reagir mais rápido.
        for card in set(player.cards):
            await message.add_reaction(card.value)

        # Função que será usada para verificar o evento de reação.
        def check(reaction, user):
            try:
                # É necessário verificar se existe uma carta com o emoji
                # reagido.
                card = Cards(str(reaction.emoji))
            except ValueError:
                # Enraiza este erro quando a reação não for uma carta
                # existente.
                return False

            # Verifica se o jogador tem a carta e se é o jogador correto
            # que reagiu.
            return card in player.cards and \
                user == player.user

        try:
            # Espera por uma reação em até 60 segundos.
            reaction, _ = await self.bot.wait_for(
                "reaction_add", check=check, timeout=60)
        except asyncio.TimeoutError:
            # Caso passe os 60 segundos, retorna `None` poiu o jogador
            # não selecionou nenhuma carta.
            return

        # Deleta a mensagem dizendo que é a vez do jogador.
        await message.delete()

        # Pega o objeto da carta.
        card = Cards(str(reaction.emoji))
        # Remove a carta do jogador.
        player.cards.remove(card)

        # Retorna a carta que o jogador selecionou.
        return card

    async def start_match(self, channel: discord.TextChannel,
                          player_one: discord.User, player_two: discord.User):
        """
        Inicia uma partida entre dois jogadores.

        Parâmetros
        ----------
        channel : discord.TextChannel
            Canal onde a partida foi iniciada.
        player_one : discord.User
            Usuário do primeiro jogador.
        player_two : discord.User
            Usuário do segundo jogador.
        """

        # Intânceia os objetos dos jogadores.
        player = Player(player_one)
        enemy = Player(player_two)

        # Avisa que a partida começou.
        await channel.send("Partida iniciada no privado de vocês, deem uma olhada!")

        # O loop irá rodar enquanto ambos jogadores estiverem vivos.
        while (not player.dead) and (not enemy.dead):
            # Faz um swap de quem é o jogador e quem é o oponente.
            player, enemy = enemy, player

            # Envia uma mensagem de aguardo para o oponente.
            message = await enemy.user.send(
                "Aguarde o turno do seu oponente!", embed=player.embed())

            try:
                # Pega a carta que o jogador escolheu para jogar.
                card = await self.get_turn_action(player)
            except discord.Forbidden:
                # Pode dar erro quando não foi possível enviar uma
                # mensagem.

                # Avisa para o outro jogador que a partida foi
                # cancelada.
                return await message.edit(content="Partida cancelada! Seu oponente demorou demais para jogar!", embed=None, delete_after=30)

            # Se o jogador não estiver escolhido uma carta
            if not card:
                # diz para o seu oponente que a partida foi cancelada.
                return await message.edit(content="Partida cancelada! Seu oponente demorou demais para jogar!", embed=None)
            else:
                # Pega a ação da carta.
                card_action = cards.get_by_name(card.name.capitalize())
                # Executa a ação da carta.
                player_result, enemy_result = await card_action.execute(player,
                                                                        enemy)
                # Envia para o outro jogador a carta que o jogador
                # escolheu e o resultado da ação da carta.
                await message.edit(content=f"O seu oponente escolheu a carta {card.name} {card.value}! {enemy_result}", embed=None, delete_after=30)
                # Envia para o jogador a carta que ele selecionou e o
                # resultado da sua ação.
                await player.user.send(f"Você usou a carta {card.name} {card.value}! {player_result}", delete_after=30)

                # Salva a carta que o jogador escolheu.
                if card != Cards.PINK:
                    player.last_card = card

                await asyncio.sleep(3)

        player_message = "Você perdeu!"
        enemy_message = "Você venceu!"
        if enemy.dead:
            player_message = "Você venceu!"
            enemy_message = "Você perdeu!"

        try:
            await player.user.send(player_message, delete_after=30)
        except discord.Forbidden:
            pass

        try:
            await enemy.user.send(enemy_message, delete_after=30)
        except discord.Forbidden:
            pass

    @commands.command(
        name="desafiar",
        aliases=["challenge",],
        usage="desafiar <oponente>",
        brief="Desafia alguém para um partida!",
        description="""
                    Bora desafiar alguém para uma partida?!
                    """
    )
    @commands.guild_only()
    async def challenge_command(self, ctx, target: discord.User) -> None:
        """
        Envia uma mensagem esperando a confirmação do oponente para
        começar a partida, para o oponente aceitar basta reagir com ✅
        na mensagem que eu enviar!

        Após a confirmação, mandarei mensagem no privado de ambos os
        jogadores!

        Argumentos
        ----------
        oponente : Membro
            Algum membro do servidor.

        Exemplos
        --------
        {prefix}desafiar <@256444020413300736>
        {prefix}desafiar black1363#0257
        {prefix}challenge DNK

        Este comando só é executado em um canal de texto de um servidor!
        O BOT precisa ter permissão para reagir em mensagens e deletar
        mensagens.
        """
        # Verifica se o oponente é o próprio jogador.
        if target == ctx.author:
            # Se for, ele não deixa a partida começar.
            return await ctx.send("Você não pode se desafiar.")

        # Verifica se o oponente é um BOT.
        if target.bot:
            # Se for, ele não deixa a partida começar.
            return await ctx.send("Você não pode desafiar um BOT!")

        # Pega a confirmação do oponente para começar a partida.
        result = await self.bot.get_emoji_confirmation(ctx.channel, target.id,
            f"{target.mention}, {ctx.author.mention} te desafiou, bora?")

        # Se o jogador negar ou não reagir, a partida é cancelada.
        if not result:
            return await ctx.send("Partida cancelada!")

        try:
            # Envia para a pessoa que pediu a partida uma mensagem.
            message_author = await ctx.author.send(f"Sua partida contra {target.mention} iniciará em instantes!", delete_after=15)
        except discord.Forbidden:
            # Se o jogador estiver com as DMs fechadas, a partida é
            # cancelada.
            return await ctx.send(f"{target.mention}, partida cancelada! {ctx.author.mention} está com o privado fechado.")

        try:
            # Tenta enviar mensagem para o oponente do jogador.
            message_target = await target.send(f"Sua partida contra {ctx.author.mention} iniciará em instantes!", delete_after=15)
        except discord.Forbidden:
            # Se o oponente estiver com as DMs fechadas, a partida é
            # cancelada.
            msg = f"{ctx.author.mention}, partida cancelada! {target.mention} está com o privado fechado."
            # Envia a mensagem enviada para o primeiro jogador.
            await message_author.edit(content=msg)
            # Envia a mensagem para o canal de origem da partida.
            return await ctx.send(msg)

        # Inicia a partida.
        await self.start_match(ctx.channel, ctx.author, target)

    @commands.command(
        name="jogo",
        aliases=["game",],
        usage="jogo"
    )
    async def game_command(self, ctx) -> None:
        msg = "O jogo é jogador contra jogador, cada um recebe 3 corações, vermelho, amarelo e verde, e começam com 5 cartas aleatórias.\n\n"

        cards_ = []
        for card in cards.all:
            e = Cards[card.__name__.upper()]
            cards_.append(f"{e.value} - **{e.name.capitalize()}**{card.__doc__}")
        cards_ = '\n'.join(cards_)

        embed = discord.Embed(color=0x8257e6, description=msg)
        embed.add_field(name="Cartas", value=cards_)

        msg = "Se as suas vidas se esgotarem, você perde e o seu oponente ganha!\n\n"
        embed.add_field(name="Extras", value=msg, inline=False)

        await ctx.send(embed=embed)

def setup(bot: t.Type[commands.Bot]) -> None:
    """
    Carrega a cog `Fun` em `bot`.

    Parâmetros
    ----------
    bot : typing.Type[commands.Bot]
        A classe ou uma subclasse do BOT.

    Raises
    ------
    commands.CommandError
        Um erro aconteceu durante o carregamento.
    """
    cog = Fun(bot)
    bot.add_cog(cog)

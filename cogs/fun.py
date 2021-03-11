from discord.ext import commands
import discord

import asyncio
import typing as t

from extension import Player
from extension.utils import Hearts, Cards


class Fun(commands.Cog):
    """
    Comandos de diversão!
    """
    def __init__(self, bot: t.Type[commands.Bot]):
        self.bot = bot

    async def get_turn_action(self, player: Player) -> t.Optional[Cards]:
        message = await player.user.send(
            "É a sua vez! Escolha a sua carta!",
            embed=player.embed())

        for card in set(player.cards):
            await message.add_reaction(card.value)

        def check(reaction, user):
            try:
                card = Cards(str(reaction.emoji))
            except ValueError:
                return False

            return card in player.cards and \
                user == player.user

        try:
            reaction, _ = await self.bot.wait_for(
                "reaction_add", check=check, timeout=60)
        except asyncio.TimeoutError:
            return

        await message.delete()

        card = Cards(str(reaction.emoji))
        player.cards.remove(card)

        return card

    async def start_match(self, channel: discord.TextChannel,
                          player_one:discord.User, player_two: discord.User):

        player = Player(player_one)
        enemy = Player(player_two)

        await channel.send("Partida iniciada no privado de vocês, deem uma olhada!")

        while (not player.dead) and (not enemy.dead):
            player, enemy = enemy, player

            message = await enemy.user.send(
                "Aguarde o turno do seu oponente!", embed=player.embed())

            try:
                card = await self.get_turn_action(player)
            except discord.Forbidden:
                try:
                    return await message.edit(content="Partida cancelada! Seu oponente demorou demais para jogar!")
                except discord.Forbidden:
                    return await channel.send(f"A partida foi cancelada, {enemy.user.mention}! {player.user.mention} demorou demais para jogar!")

            if not card:
                try:
                    await message.edit(content="Partida cancelada! Seu oponente demorou demais para jogar!")
                except discord.Forbidden:
                    return await channel.send(f"A partida foi cancelada, {enemy.user.mention}! {player.user.mention} demorou demais para jogar!")
            else:
                await message.edit(content=f"O seu oponente escolheu a carta {card.name} {card.value}!", delete_after=30)

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
        result = await self.bot.get_emoji_confirmation(ctx.channel, target.id,
            f"{target.mention}, {ctx.author.mention} te desafiou, bora?")

        if not result:
            return await ctx.send("Partida cancelada!")

        try:
            message_author = await ctx.author.send(f"Sua partida contra {target.mention} iniciará em instantes!", delete_after=15)
        except discord.Forbidden:
            return await ctx.send(f"{target.mention}, partida cancelada! {ctx.author.mention} está com o privado fechado.")

        try:
            message_target = await target.send(f"Sua partida contra {ctx.author.mention} iniciará em instantes!", delete_after=15)
        except discord.Forbidden:
            msg = f"{ctx.author.mention}, partida cancelada! {target.mention} está com o privado fechado."
            await message_author.edit(content=msg)
            return await ctx.send(msg)

        await self.start_match(ctx.channel, ctx.author, target)

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

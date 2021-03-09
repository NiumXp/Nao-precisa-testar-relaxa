from discord.ext import commands
import discord

import typing as t


class Fun(commands.Fun):
    """
    Comandos de diversão!
    """

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
        await ctx.send(
            f"{target.mention}, {ctx.author.mention} te desafiou, você topa?")

        result = await self.bot.get_emoji_confirmation(ctx.channel, ctx.author.id,
            f"{target.mention}, {ctx.author.mention} te desafiou, bora?")

        if not result:
            return


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

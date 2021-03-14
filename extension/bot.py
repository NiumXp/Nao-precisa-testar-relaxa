from discord.ext.commands import Bot, errors
import discord

import asyncio
import typing as t

from extension import utils

CHECK_MARK_EMOJI = utils.emoji("CHECK_MARK")
CROSS_EMOJI = utils.emoji("CROSS")


class CardBot(Bot):
    """
    CardBot é um BOT que implementa um jogo simples como o jogo da velha
    e estratégico como UNO.

    Para jogar basta usar o comando `desafiar` e para saber as regras do
    jogo basta usar o comando `jogo`.
    """

    def __init__(self, prefix, *args, **kwargs):
        super().__init__(*args, **kwargs, description=self.__doc__)
        self.normal_prefix = prefix

    async def on_ready(self):
        """Imprime `I'm ready!` no terminal."""
        print("I'm ready!")

    async def on_message(self, message):
        if message.content in [f"<@{self.user.id}>", f"<@!{self.user.id}>"]:
            msg = f"Olá, {message.author.mention}! Utilize o comando `{self.normal_prefix}ajuda` se precisar de ajuda!"
            return await message.channel.send(msg)
        return await self.process_commands(message)

    async def on_command_error(self, ctx, error):
        base = f"Digite `{ctx.prefix}ajuda {ctx.invoked_with}` para ver como utilizar este comando."
        if isinstance(error, errors.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention}, você usou o comando de forma errada! {base}")
        elif isinstance(error, errors.BotMissingPermissions):
            await ctx.send("Eu não tenho permissão para executar este comando! " + base)
        else:
            raise error

    async def get_emoji_confirmation(self, channel: discord.TextChannel,
                                     user_id: int, message: str, *,
                                     timeout: int=60) -> t.Optional[bool]:
        """
        Envia uma mensagem com o conteúdo `message` para `channel`,
        reage com `CHECK_MARK_EMOJI` e `CROSS_EMOJI` na mensagem e
        espera `timeout` segundos até o usuário com id `user_id` reagir.

        Parâmetros
        ----------
        channel : discord.TextChannel
            Canal de texto onde a confirmação será feita.
        message : str
            Mensagem que será mostrada na mensagem de confirmação.
        user_id : int
            Discord ID do usuário que fará a confirnação.
        timeout : int (60)
            Tempo limite em segundos para aguardar a confirmação.

        Raises
        ------
        discord.HTTPException
            Não foi possível enviar a mensagem.
        discord.Forbidden
            O BOT não teve permissão para enviar a mensagem em `channel`
            ou reagir com os emojis na mensagem.

        Retorno
        -------
        typing.Optional[bool]
            Retorna `None` se o `timeout` esgotou, caso contrário,
            retorna um `bool` como resposta de `user_id`.
        """
        # Envia a mensagem no canal de texto.
        message = await channel.send(content=message)

        # Adiciona os emojis de confirmação na mensagem.
        await message.add_reaction(CHECK_MARK_EMOJI)
        await message.add_reaction(CROSS_EMOJI)

        def check(reaction, user) -> bool:
            # Checa se a pessoa que reagiu é a pessoa correta para a
            # confirmação.

            # Verifica se o usuário que reagiu é o esperado.
            # Verifica se a reação foi na mensagem do BOT.
            # Verifica se o emoji reagido é um emoji de confirmação.
            return user.id == user_id and \
                reaction.message.id == message.id and \
                    str(reaction.emoji) in [CHECK_MARK_EMOJI, CROSS_EMOJI]

        try:
            # Espera por uma reação do usuário durante `timeout`
            # segundos.
            reaction, _ = await self.wait_for(
                "reaction_add", check=check, timeout=timeout)
        except asyncio.TimeoutError:
            # Retorna None pois o usuário demorou demais para reagir.
            return None
        finally:
            try:
                # Deleta a mensagem de confirmação.
                await message.delete()
            except discord.NotFound:
                # A mensagem pode ter sido apagada.
                pass

        # Retorna dizendo se o emoji reagido é `CHECK_MARK_EMOJI`.
        return str(reaction.emoji) == CHECK_MARK_EMOJI

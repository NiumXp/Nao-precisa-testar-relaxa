from discord.ext.commands import Bot
import discord

import asyncio
import typing as t

CHECK_MARK_EMOJI = "✅"
CROSS_EMOJI = "❌"


class CardBot(Bot):
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
            return user.id == user_id and \
                # Verifica se a reação foi na mensagem do BOT.
                reaction.message.id == message.id and \
                    # Verifica se o emoji reagido é um emoji de
                    # confirmação.
                    str(reaction.emoji) in [CHECK_MARK_EMOJI, CROSS_EMOJI]

        try:
            # Espera por uma reação do usuário durante `timeout`
            # segundos.
            reaction, _ = await self.wait_for(
                "reaction_add", check=check, timeout=timeout)
        except asyncio.TimeoutError:
            # Retorna None pois o usuário demorou demais para reagir.
            return None

        # Retorna dizendo se o emoji reagido é `CHECK_MARK_EMOJI`.
        return str(reaction.emoji) == CHECK_MARK_EMOJI

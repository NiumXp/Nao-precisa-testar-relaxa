# Carrega as váriaves no arquivo .env
from dotenv import load_dotenv
load_dotenv()

from discord.ext.commands import when_mentioned_or
import discord

import os
import re
import traceback

from extension import CardBot

# Instânceia a classe do BOT e passa o prefixo declarado na variável de
# ambiente.
bot_prefix = os.environ["BOT_PREFIX"]
bot = CardBot(bot_prefix, help_command=None,
              command_prefix=when_mentioned_or(bot_prefix))

# Comando de help
@bot.command(
    name="ajuda",
    aliases=["help",],
    usage="help (cmd)",
    brief="Veja sobre alguns comandos!"
)
async def help_command(ctx, *, cmd: str = None):
    """Mostra algumas informações sobre comandos e o BOT."""

    if not cmd:
        commands = enumerate(c for c in bot.walk_commands())
        commands = [f"[{i}] {bot_prefix}{c.usage}" for i, c in commands]
        commands = '\n'.join(commands)

        embed = discord.Embed(
            description=f"{bot.description}**```ini\nUtilize {bot_prefix}help `commando` para saber mais sobre um commando específico.\n\n[Comandos]\n{commands}\n\n[Legenda]\n<> argumento obrigatório\n() argumento opcional```**",
            timestamp=ctx.message.created_at,
            color=ctx.author.color
        )
        return await ctx.send(embed=embed)
    else:
        # Checks if it's a command
        cmd = cmd.lower()
        command = bot.get_command(cmd)
        if command:
            command_embed = discord.Embed(
                title=command.name,
                description=f"{command.brief} {command.description} ```{command.help.replace('prefix', ctx.prefix)}```",
                color=ctx.author.color,
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=command_embed)

        # Otherwise, it's an invalid parameter (Not found)
        else:
            await ctx.send(f"**Não encontrei o comando `{cmd}`!**")

# Percorre o diretório `cogs` para carregar todos os comandos do BOT.
for dirpath, _, filenames in os.walk("cogs"):
    for filename in filenames:
        # `filename` é o nome de um arquivo, pra cara um que for
        # encontrado, é necessário verificar se este tem extensão `.py`
        # e se não começa com `_`.
        name, ext = os.path.splitext(filename)
        # Se o arquivo começar com `_` ele não deverá ser carregado,
        # isso é necessário para caso você não queira carregar
        # o arquivo.
        if not name.startswith('_') and ext == ".py":
            # Pega o camminho real do arquivo.
            dirpath = os.path.join(dirpath, name)
            # Transformar barra e contra barra em ponto.
            dirpath = re.sub(r"/+|\\+", '.', dirpath)
            # Carrega a cog.
            bot.load_extension(dirpath)

# Roda o BOT usando o token defino nas variáveis de ambiente.
bot.run(os.environ["BOT_DISCORD_TOKEN"])

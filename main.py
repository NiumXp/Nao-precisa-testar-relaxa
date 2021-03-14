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
improved_bot_prefix = when_mentioned_or(bot_prefix)
bot = CardBot(improved_bot_prefix, help=None)

# Comando de help
@bot.command()
async def help(ctx, *, cmd: str = None):
  """ Mostra algumas informações sobre comandos e categorias. """
  
  if not cmd:
      embed = discord.Embed(
      title="Todos comandos e categorias",
      description=f"```ini\nUtilize {bot_prefix}help `commando` ou {bot_prefix}help `categoria` para saber mais sobre um commando ou categoria específica\n[Exemplos]\n[1] Categoria: {bot_prefix}help fun\n[2] Commando: {bot_prefix}help desafiar```",
      timestamp=ctx.message.created_at,
      color=ctx.author.color
      )

      for cog in bot.cogs:
          cog = bot.get_cog(cog)
          commands = [c.qualified_name for c in cog.get_commands() if not c.hidden]
          subcommands = []
          for c in cog.get_commands():
              try:
                for sb in c.commands:
                  if not c.hidden:
                    subcommands.append(sb.qualified_name)
              except AttributeError:
                pass

          if commands:
            text = f"`Comandos:` {', '.join(commands)}" 
            if subcommands:
              text += f"\n`Subcomandos:` {', '.join(subcommands)}"
            embed.add_field(
            name=f"__{cog.qualified_name}__",
            value=text,
            inline=False
            )

      cmds = []
      for y in bot.walk_commands():
          if not y.cog_name and not y.hidden:
              cmds.append(y.name)
      embed.add_field(
      name='__Comandos Não-Categorizados__', 
      value=f"`Comandos:` {', '.join(cmds)}", 
      inline=False)
      await ctx.send(embed=embed)

  else:
    # Checks if it's a command
    if command := bot.get_command(cmd.lower()):
      command_embed = discord.Embed(title=f"__Comando:__ {command.name}", description=f"__**Descrição:**__\n```{command.help}```", color=ctx.author.color, timestamp=ctx.message.created_at)
      return await ctx.send(embed=command_embed)

    for cog in bot.cogs:
      if str(cog).lower() == str(cmd).lower():
          cog = bot.get_cog(cog)
          cog_embed = discord.Embed(title=f"__Categoria:__ {cog.qualified_name}",
          color=ctx.author.color, timestamp=ctx.message.created_at)
          commands = []
          subcommands = []
          for c in cog.get_commands():
              if not c.hidden:
                  commands.append(c.name)
              try:
                for sb in c.commands:
                  if not c.hidden:
                    subcommands.append(sb.qualified_name)
              except AttributeError:
                pass

          cog_embed.description = f"__**Descrição:**__\n```{cog.description}```\n`Comandos:` {', '.join(commands)}\n\n`Subcomando:` {', '.join(subcommands)}"

          return await ctx.send(embed=cog_embed)

    # Otherwise, it's an invalid parameter (Not found)
    else:
      await ctx.send(f"**Parâmetro inválido! `{cmd}` não é nem um comando, nem uma categoria!**")








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

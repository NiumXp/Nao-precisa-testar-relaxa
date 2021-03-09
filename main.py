# Carrega as váriaves no arquivo .env
from dotenv import load_dotenv
load_dotenv()

import os
import re
import traceback

from extension import CardBot, asset

# Instânceia a classe do BOT e passa o prefixo declarado na variável de
# ambiente.
bot = CardBot(os.environ["BOT_PREFIX"])

# Registra o evento de quando o BOT estiver pronto.
@bot.event
async def on_ready():
    # Imprime uma mensagem apenas para sabermos se o BOT está ligado.
    print("I'm ready!")

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

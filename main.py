
# Carrega as váriaves no arquivo .env
from dotenv import load_dotenv
load_dotenv()

import os

from extension import CardBot

bot = CardBot(os.environ["BOT_PREFIX"])

@bot.event
async def on_ready():
    print("I'm ready!")

bot.run(os.environ["BOT_DISCORD_TOKEN"])

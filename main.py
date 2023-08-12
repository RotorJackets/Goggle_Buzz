import discord
import time
from discord.ext import commands
from secret import bot_token, application_id

from config import config


class MyBot(commands.Bot):
    async def setup_hook(self):
        for ext in config["cogs"]:
            await self.load_extension(ext)

    async def on_ready(self):
        await self.wait_until_ready()
        await self.change_presence(
            status=discord.Status.idle,
            activity=discord.Activity(
                name="Velocidrone",
                # url="https://www.velocidrone.com/",
                type=discord.ActivityType.custom,
                state="Destroying the competition!",
                details="Destroying the competition!",
                # timestamps={"start": time.time()},
                # buttons=["https://www.velocidrone.com/"],
            ),
        )
        print(f"{self.user} has connected to Discord!")


bot = MyBot(
    command_prefix=config["command_prefix"],
    intents=discord.Intents.all(),
    application_id=application_id,
)

bot.run(bot_token)

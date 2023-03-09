import discord
import random
from discord.ext import commands
from discord import app_commands
from discord.utils import get
from api_key import bot_token

# Version 1.0
# Testing Server id = 473695678690885632
# RotorJackets id = 723199784697200810

guilds = [discord.Object(id=473695678690885632), discord.Object(id=723199784697200810)]
fight_song_quotes = [
    "I'm a Ramblin' Wreck from Georgia Tech, and a hell of an engineer",
    "Oh! If I had a daughter, sir, I'd dress her in White and Gold",
    "But if I had a son, sir, He would yell, 'To hell with Georgia!' like his daddy used to do.",
    "Oh, I wish I had a barrel of rum and sugar three thousand pounds,",
    "I'm a ramblin', gamblin', hell of an engineer! ",
    "Like all the jolly good fellows, I drink my whiskey clear.",
    "For I'm a rambling rake of poverty. And the son of a gambolier. ",
    "I'm a son of a, son of a, son of a, son of a, son of a DKE!",
    "He'd yell: 'TO HELL WITH BOULDER!'",
    "I'm a rambling wreck from Golden Tech, a helluva engineer. ",
    "I'm a rambling wreck from Rapid Tech, and a helluva engineer. Hey! ",
    'He would yell "To Hell" with Delaware And yell for O. S. U. ',
    "If I had a daughter, I'd dress her up in green, I'd send her on the campus to coach the Freshman team;",
    "I'm a moral wreck from the Polytech",
    "He fed me all those V-Dogs, and pitchers & pitchers of beer,",
    "Studenter i den gamle stad, ta vare på byens ry!",
    "La'kke byen få ro, men la den få merke det er en studenterby!",
    "Og øl og dram, og øl og dram, og øl og dram, og øl og dram.",
]


class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())

    async def on_ready(self):
        await self.wait_until_ready()
        print(f"We have logged in as: {self.user}.")


bot = client()
tree = app_commands.CommandTree(bot)


# Commands
@bot.event
async def on_message(message):
    if message.author == client.user:
        return

    if "!sync" in message.content.lower():
        await tree.sync()
        await message.channel.send("Synced")
        print("Command tree synced.")


@tree.command(name="test_input")
async def test_input(interaction: discord.Interaction, number: int, string: str):
    await interaction.response.send_message(
        f"Modify {number=} {string=}", ephemeral=True
    )


@tree.command(name="test_options")
@app_commands.describe(option="This is a description of what the option means")
@app_commands.choices(
    option=[
        app_commands.Choice(name="Option 1", value="1"),
        app_commands.Choice(name="Option 2", value="2"),
    ]
)
async def test_options(
    interaction: discord.Interaction, option: app_commands.Choice[str]
):
    pass


@tree.command(name="fight_song")
async def test_input(interaction: discord.Interaction):
    await interaction.channel.send(random.choice(fight_song_quotes))


bot.run(bot_token)

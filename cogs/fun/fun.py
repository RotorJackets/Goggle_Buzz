import discord
import random

from discord import app_commands
from discord.ext import commands

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
    "https://media.discordapp.net/attachments/604866125209272331/846498885718507530/image0.gif",
    "https://cdn.discordapp.com/attachments/1028015791028846652/1078527921863536772/buzz.mp4",
    "(╯°□°)╯︵ ┻━┻",
    "ヘ(◕。◕ヘ)",
]


class Fun(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="fight_song",
        description="Sends a random fight song quote",
    )
    async def fight_song(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            random.choice(fight_song_quotes), ephemeral=False
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))

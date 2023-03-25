import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get

from config import config as config_main

config = config_main["util"]


class RoleOptions(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(
        label="@ GT",
        style=discord.ButtonStyle.grey,
        emoji="<:gogglesbuzz:753465023560679484>",
    )
    async def option_one(
        self, interaction: discord.Interaction, button: discord.ui.button
    ):
        rotor = get(interaction.guild.roles, name="RotorJacket")
        if rotor in interaction.user.roles:
            await interaction.user.remove_roles(rotor)
            await interaction.response.send_message(
                "RotorJacket role removed", ephemeral=True
            )
        else:
            await interaction.user.add_roles(rotor)
            await interaction.response.send_message(
                "https://cdn.discordapp.com/attachments/534939044078157834/1086736052670173295/IMG_3452.jpg",
                ephemeral=True,
            )

    @discord.ui.button(
        label="Not @ GT",
        style=discord.ButtonStyle.grey,
        emoji="<a:bigthink:753469546526146632>",
    )
    async def option_2(
        self, interaction: discord.Interaction, button: discord.ui.button
    ):
        friend = get(interaction.guild.roles, name="Friend of Rotorjackets")
        if friend in interaction.user.roles:
            await interaction.user.remove_roles(friend)
            await interaction.response.send_message(
                "Friend of RotorJackets role removed", ephemeral=True
            )
        else:
            await interaction.user.add_roles(friend)
            await interaction.response.send_message(
                "https://cdn.discordapp.com/attachments/534939044078157834/1086736052670173295/IMG_3452.jpg",
                ephemeral=True,
            )

    @discord.ui.button(
        label="Racer",
        style=discord.ButtonStyle.grey,
        emoji="🏁",
    )
    async def option_3(
        self, interaction: discord.Interaction, button: discord.ui.button
    ):
        racer = get(interaction.guild.roles, name="racer")
        if racer in interaction.user.roles:
            await interaction.user.remove_roles(racer)
            await interaction.response.send_message(
                "Racer Role removed", ephemeral=True
            )
        else:
            await interaction.user.add_roles(racer)
            await interaction.response.send_message(
                "Pilots arm your quads", ephemeral=True
            )

    @discord.ui.button(
        label="Sim Pings",
        style=discord.ButtonStyle.grey,
        emoji="📺",
    )
    async def option_4(
        self, interaction: discord.Interaction, button: discord.ui.button
    ):
        sim = get(interaction.guild.roles, name="sim")
        if sim in interaction.user.roles:
            await interaction.user.remove_roles(sim)
            await interaction.response.send_message("Sim Role removed", ephemeral=True)
        else:
            await interaction.user.add_roles(sim)
            await interaction.response.send_message(
                "Update your Velocidrone", ephemeral=True
            )


@app_commands.guild_only()
class RoleSelection(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="intro",
        description="Generate new intro message",
    )
    async def intro(self, interaction: discord.Interaction):
        welcome_channel = self.bot.get_channel(config["welcome_channel"])
        embed = discord.Embed(color=discord.Color.gold())
        embed.set_author(name=f"Welcome to RotorJackets")
        embed.set_thumbnail(url=(welcome_channel.guild.icon))
        embed.add_field(
            name="This server is the primary point of communication for RotorJackets.",
            value="Open to all who love drones\n\n"
            "If you want to race please join our MultiGP chapter here: https://www.multigp.com/chapters/view/?chapter=RotorJackets\n\n"
            "1. Post an introduction in #introductions\n"
            "2. Checkout #new-member-info\n"
            "3. Any FPV video you want to plug, you can do so in #shameless-plug\n\n"
            "Select your roles with the buttons below",
        )

        view = RoleOptions()
        await welcome_channel.send(embed=embed, view=view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RoleSelection(bot))

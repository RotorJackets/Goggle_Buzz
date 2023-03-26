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
    )
    async def option_one(
        self, interaction: discord.Interaction, button: discord.ui.button
    ):
        rotor = get(interaction.guild.roles, name="RotorJacket")
        if rotor in interaction.user.roles:
            await interaction.user.remove_roles(rotor)
            await interaction.response.send_message("Sadge", ephemeral=True)
        else:
            await interaction.user.add_roles(rotor)
            await interaction.response.send_message(
                "https://cdn.discordapp.com/attachments/534939044078157834/1086736052670173295/IMG_3452.jpg",
                ephemeral=True,
            )

    @discord.ui.button(
        label="Not @ GT",
        style=discord.ButtonStyle.grey,
    )
    async def option_2(
        self, interaction: discord.Interaction, button: discord.ui.button
    ):
        friend = get(interaction.guild.roles, name="Friend of Rotorjackets")
        if friend in interaction.user.roles:
            await interaction.user.remove_roles(friend)
            await interaction.response.send_message("Goodbye Friend", ephemeral=True)
        else:
            await interaction.user.add_roles(friend)
            await interaction.response.send_message(
                "https://cdn.discordapp.com/attachments/534939044078157834/1086736052670173295/IMG_3452.jpg",
                ephemeral=True,
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
        welcome_channel = get(interaction.guild.text_channels, name="welcome")
        embed = discord.Embed(color=discord.Color.random())
        embed.set_author(name=f"Welcome to RotorJackets")
        embed.add_field(
            name="This server is the primary point of communication for RotorJackets.",
            value="Open to all who love drones\n\n"
            "If you want to race please join our MultiGP chapter here: https://www.multigp.com/chapters/view/?chapter=RotorJackets\n\n"
            "1. Post an introduction in introductions\n"
            "2. Checkout new-member-info\n"
            "3. Any FPV video you want to plug, you can do so in shameless-plug\n\n"
            "Select your roles with the buttons below",
        )

        view = RoleOptions()
        await welcome_channel.send(embed=embed, view=view)
        await interaction.response.send_message("Sent intro message", 
                                                
                                                
                                                ephemeral=True)





async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RoleSelection(bot))

import discord
from discord import app_commands, ChannelType
from discord.ext import commands
from discord.utils import get
from discord.ui import Button

from lib.config import config

class Welcome(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(
        label = "@ GT",
        style = discord.ButtonStyle.grey,
    )
    async def welcome1(self, interaction: discord.Interaction, button: discord.ui.button):
        rotor = get(interaction.guild.roles, name = 'RotorJacket')
        if rotor in interaction.user.roles:
            await interaction.user.remove_roles(rotor)
            await interaction.response.send_message("Sadge", ephemeral=True)
        else:
            await interaction.user.add_roles(rotor)
            await interaction.response.send_message(
                "https://cdn.discordapp.com/attachments/534939044078157834/1086736052670173295/IMG_3452.jpg",
                ephemeral=True)

    @discord.ui.button(
        label="Not @ GT",
        style=discord.ButtonStyle.grey,
    )
    async def welcome2(self, interaction: discord.Interaction, button: discord.ui.button):
        friend = get(interaction.guild.roles, name='Friend of Rotorjackets')
        if friend in interaction.user.roles:
            await interaction.user.remove_roles(friend)
            await interaction.response.send_message("Goodbye Friend", ephemeral=True)
        else:
            await interaction.user.add_roles(friend)
            await interaction.response.send_message(
                "https://cdn.discordapp.com/attachments/534939044078157834/1086736052670173295/IMG_3452.jpg",
                ephemeral=True)




class Util(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        shipping_channel = get(message.guild.text_channels, name = "shipping-sharing")
        if (message.channel.id == shipping_channel.id):
            await message.channel.create_thread(name=f"{message.author} is ordering goods",
                                                type=ChannelType.public_thread)
    @app_commands.command(
        name = "new_order",
        description = "Create a new group order",
    )
    async def new_order(self, interaction: discord.Interaction, website: str = None):
        role = get(interaction.guild.roles, name = 'RotorJacket')
        if role not in interaction.user.roles:
            await interaction.response.send_message('You must be a RotorJacket to create a group order')
        else:
            channel = get(interaction.guild.text_channels, name = "shipping-sharing")
            if website == None:
                await channel.create_thread(name = f"{interaction.user} is ordering goods", type = ChannelType.public_thread)
            else:
                await channel.create_thread(name=f"{interaction.user} is ordering goods from {website}",
                                            type=ChannelType.public_thread)
            await interaction.response.send_message(f'Group order created in {channel}')

    @app_commands.command(
        name = "intro",
        description = "Generate new intro message",
    )
    async def intro(self, interaction: discord.Interaction):

        welcome_channel = get(interaction.guild.text_channels, name = 'welcome')
        embed = discord.Embed(color=discord.Color.random())
        embed.set_author(name=f"Welcome to RotorJackets")
        embed.add_field(name="This server is the primary point of communication for RotorJackets.",
                        value="Open to all who love drones\n\n"
                              "If you want to race please join our MultiGP chapter here: https://www.multigp.com/chapters/view/?chapter=RotorJackets\n\n"
                              "1. Post an introduction in introductions\n"
                              "2. Checkout new-member-info\n"
                              "3. Any FPV video you want to plug, you can do so in shameless-plug\n\n"
                              "Select your roles with the buttons below")

        view = Welcome()
        await welcome_channel.send(embed= embed, view=view)



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Util(bot))
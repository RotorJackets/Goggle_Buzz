import discord
from discord import app_commands, ChannelType
from discord.ext import commands
from discord.utils import get
from discord.ui import Button
from config import config as config_main

config = config_main["util"]


class OrderOptions(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(
        label="Goods Ordered",
        style=discord.ButtonStyle.green,
        emoji="<a:Verify:940328302420295730>",
    )
    async def option_one(
        self, interaction: discord.Interaction, button: discord.ui.button
    ):
        shipping_channel = get(interaction.guild.text_channels, name="shipping-sharing")
        await interaction.channel.edit(locked=True)
        await shipping_channel.send(
            f"Goods for {interaction.user}'s group order has been ordered!"
        )
        pass

    @discord.ui.button(
        label="Cancel Order",
        style=discord.ButtonStyle.danger,
        emoji="⛔",
    )
    async def option_two(
        self, interaction: discord.Interaction, button: discord.ui.button
    ):
        shipping_channel = get(interaction.guild.text_channels, name="shipping-sharing")
        print(interaction.channel)
        await interaction.channel.edit(locked=True)
        await shipping_channel.send(
            f"{interaction.user}'s group order has been canceled!"
        )


@app_commands.guild_only()
class Shipping(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        shipping_channel = get(message.guild.text_channels, name="shipping-sharing")
        if message.channel.id == shipping_channel.id:
            thread = await message.channel.create_thread(
                name=f"{message.author} is ordering goods",
                type=ChannelType.public_thread,
            )
            embed = discord.Embed(
                color=discord.Color.gold(),
                title="Group Order",
                description="Complete your group order with the buttons below",
            )
            view = OrderOptions()
            msg = await thread.send(embed=embed, view=view)
            await msg.pin()

    @app_commands.command(
        name="new_order",
        description="Create a new group order",
    )
    async def new_order(self, interaction: discord.Interaction, website: str = None):
        role = get(interaction.guild.roles, name=config["order_role"])
        thread = 0
        if role not in interaction.user.roles:
            await interaction.response.send_message(
                "You must be a RotorJacket to create a group order"
            )
        else:
            # TODO: Switch to using channel ID instead of name
            channel = get(
                interaction.guild.text_channels, name=config["shipping_channel"]
            )
            if website == None:
                thread = await channel.create_thread(
                    name=f"{interaction.user} is ordering goods",
                    type=ChannelType.public_thread,
                )
            else:
                thread = await channel.create_thread(
                    name=f"{interaction.user} is ordering goods from {website}",
                    type=ChannelType.public_thread,
                )
            await interaction.response.send_message(f"Group order created in {channel}")
            embed = discord.Embed(
                color=discord.Color.gold(),
                title="Group Order",
                description="Complete your group order with the buttons below",
            )
            view = OrderOptions()
            msg = await thread.send(embed=embed, view=view)
            await msg.pin()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Shipping(bot))

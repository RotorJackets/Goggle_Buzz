import discord
from discord import app_commands
from discord.ext import commands, tasks

import cogs.leaderboard.leaderboard_helper as leaderboard_helper
from config import config as config_main

config = config_main["leaderboard"]


@app_commands.guild_only()
class Leaderboard(commands.GroupCog, name="leaderboard"):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        leaderboard_helper.setup()
        self.background_leaderboard_save.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if (
            level := leaderboard_helper.adjust_xp(message.guild, message.author)
        ) is not None:
            await message.channel.send(
                f"{message.author.mention} has leveled up to level {level}"
            )

    @app_commands.command(
        name="show",
        description="Shows the leaderboard",
    )
    async def show(self, interaction: discord.Interaction):
        leaders = leaderboard_helper.get_leaders(interaction.guild)
        leaderboard_output = """"""

        for i in range(len(leaders)):
            leaderboard_output += f"""\nLevel {leaders[i][1]["level"]}:   {self.bot.get_user(int(leaders[i][0]))}"""

        if len(leaderboard_output) == 0:
            leaderboard_output = "No one is on the leaderboard yet!"

        await interaction.response.send_message(
            leaderboard_output,
            ephemeral=False,
            # delete_after=config["leaderboard_delete_after_seconds"],
        )

    @app_commands.command(
        name="level",
        description="Shows your level or the level of another user",
    )
    @app_commands.describe(member="The user to show the level of, defaults to yourself")
    async def level(
        self, interaction: discord.Interaction, member: discord.Member = None
    ):
        if member is None:
            member = interaction.user

        member_info = leaderboard_helper.get_info(interaction.guild, member)
        await interaction.response.send_message(
            f"""**{member.mention}** is in **{member_info["place"]}** place on the leaderboard! """
            + f"""They are level **{member_info["level"]}** and are """
            + f"""**{member_info["xp"]/config["level_up_XP"] * 100:3.2f}%** to the next level!""",
            ephemeral=True,
        )

    @app_commands.command(
        name="save",
        description="Saves the leaderboard",
    )
    @commands.has_permissions(administrator=True)
    async def save(self, interaction: discord.Interaction):
        leaderboard_helper.save(interaction.guild)
        await interaction.response.send_message(
            f"Leaderboard for **{interaction.guild.name}** has been saved.",
            ephemeral=True,
        )

    @app_commands.command(
        name="reset",
        description="Resets the leaderboard",
    )
    @commands.has_permissions(administrator=True)
    async def reset(self, interaction: discord.Interaction):
        leaderboard_helper.reset_guild(interaction.guild)
        await interaction.response.send_message(
            f"Leaderboard for **{interaction.guild.name}** has been reset.",
            ephemeral=True,
        )

    @app_commands.command(
        name="reset_member_xp",
        description="Resets the leaderboard",
    )
    @commands.has_permissions(administrator=True)
    async def reset_member_xp(
        self, interaction: discord.Interaction, member: discord.Member
    ):
        leaderboard_helper.reset_member(member)
        await interaction.response.send_message(
            f"XP for **{member.name}** has been reset.",
            ephemeral=True,
        )

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sync(self, ctx):
        print("Syncing")
        await self.bot.tree.sync()
        print("Synced")
        await ctx.send("Synced")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def save(self, ctx):
        leaderboard_helper.save(ctx.guild)
        await ctx.send("Saved")

    @tasks.loop(seconds=config["leaderboard_save_interval_seconds"], count=None)
    async def background_leaderboard_save(self):
        leaderboard_helper.save(config_main["guilds"])


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Leaderboard(bot))

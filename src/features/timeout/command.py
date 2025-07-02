"""
Timeout slash command - separated from functionality.
"""
import discord
from src.res import R
from src.features.timeout.timeout import timeout_user


def setup_timeout_command(bot: discord.Bot):
    """
    Setup the timeout command for the bot.
    Args:
        bot (discord.Bot): The Discord bot instance.
    """

    @bot.slash_command(
        name="timeout",
        description=R.timeout_command_desc,
        default_member_permissions=discord.Permissions(moderate_members=True)
    )
    @discord.default_permissions(administrator=True)
    @discord.option("user", description=R.timeout_user_desc, type=discord.SlashCommandOptionType.user, required=True)
    @discord.option("duration", description=R.timeout_duration_desc, type=discord.SlashCommandOptionType.string, required=True)
    @discord.option("reason", description=R.timeout_reason_desc, type=discord.SlashCommandOptionType.string, required=False)
    async def timeout_command(interaction: discord.Interaction, user: discord.Member, duration: str, reason: str = None):
        """Timeouts a user for a specified duration."""
        await timeout_user(interaction, user, duration, reason)

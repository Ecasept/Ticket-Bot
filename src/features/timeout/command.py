"""
Timeout slash command - separated from functionality.
"""
import discord
from src.res import R, RD, RL
from src.features.timeout.timeout import timeout_user
from src.custom_bot import CustomBot


def setup_timeout_command(bot: CustomBot):
    """
    Setup the timeout command for the bot.
    Args:
        bot (CustomBot): The Discord bot instance.
    """

    @bot.slash_command(
        name=RD.command.timeout.name,
        name_localizations=RL.command.timeout.name,
        description=RD.command.timeout.desc,
        description_localizations=RL.command.timeout.desc,
        default_member_permissions=discord.Permissions(moderate_members=True)
    )
    @discord.default_permissions(administrator=True)
    @discord.option(
        parameter_name="user",
        name=RD.command.timeout.option.user,
        name_localizations=RL.command.timeout.option.user,
        description=RD.command.timeout.option.user_desc,
        description_localizations=RL.command.timeout.option.user_desc,
        type=discord.SlashCommandOptionType.user,
        required=True
    )
    @discord.option(
        parameter_name="duration",
        name=RD.command.timeout.option.duration,
        name_localizations=RL.command.timeout.option.duration,
        description=RD.command.timeout.option.duration_desc,
        description_localizations=RL.command.timeout.option.duration_desc,
        type=discord.SlashCommandOptionType.string,
        required=True
    )
    @discord.option(
        parameter_name="reason",
        name=RD.command.timeout.option.reason,
        name_localizations=RL.command.timeout.option.reason,
        description=RD.command.timeout.option.reason_desc,
        description_localizations=RL.command.timeout.option.reason_desc,
        type=discord.SlashCommandOptionType.string,
        required=False
    )
    async def timeout_command(interaction: discord.Interaction, user: discord.Member, duration: str, reason: str = None):
        """Timeouts a user for a specified duration."""
        await timeout_user(interaction, user, duration, reason)

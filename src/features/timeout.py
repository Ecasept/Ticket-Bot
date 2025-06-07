import discord
import datetime
from src.res import R, C
from src.utils import create_embed, get_timeout_log_channel, handle_error, logger, error_embed, parse_duration
from src.database import db


async def send_timeout_log(interaction: discord.Interaction, user: discord.Member, duration_delta: datetime.timedelta, reason: str | None, log_channel: discord.TextChannel):
    """Sends a log message to the configured timeout log channel."""

    description_lines = [
        f"**{R.timeout_log_user}**: {user.mention}",
        f"**{R.timeout_log_duration}**: `{str(duration_delta)}`",
        f"**{R.timeout_log_reason}**: {reason if reason else R.timeout_log_no_reason}",
        f"**{R.timeout_log_moderator}**: {interaction.user.mention}"
    ]
    description = "\n".join(description_lines)

    embed = discord.Embed(
        title=R.timeout_log_title,
        description=description,
        color=C.warning_color,
        timestamp=datetime.datetime.now(datetime.timezone.utc)
    )

    await log_channel.send(embed=embed)


def setup_timeout_commands(bot: discord.Bot):
    """
    Sets up the timeout slash command.
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
        await interaction.response.defer(ephemeral=True)

        duration, err = parse_duration(duration)
        if err:
            await handle_error(interaction, err)
            return
        duration_delta = datetime.timedelta(seconds=duration)

        if duration > C.timeout_max_duration:
            await interaction.followup.send(embed=error_embed(R.timeout_duration_too_long), ephemeral=True)
            logger.info(
                f"{interaction.user.name} tried to timeout {user.name} for too long", interaction)
            return

        if user == interaction.user:
            await interaction.followup.send(embed=error_embed(R.timeout_cant_timeout_self), ephemeral=True)
            logger.info(
                f"{interaction.user.name} tried to timeout themselves", interaction)
            return

        if user == bot.user:
            await interaction.followup.send(embed=error_embed(R.timeout_cant_timeout_bot), ephemeral=True)
            logger.info(
                f"{interaction.user.name} tried to timeout the bot", interaction)
            return

        log_channel, err = await get_timeout_log_channel(interaction.guild)
        if err:
            await handle_error(interaction, err)
            return

        end = datetime.datetime.now(datetime.timezone.utc) + duration_delta

        await user.timeout(end, reason=reason)
        success_msg = R.timeout_success % (user.mention, str(
            duration_delta), reason) if reason else R.timeout_success_no_reason % (user.mention, str(duration_delta))
        await interaction.followup.send(embed=create_embed(success_msg, color=C.success_color), ephemeral=True)
        logger.info(
            f"{interaction.user.name} timed out {user.name} for {duration_delta}. Reason: {reason if reason else 'None'}", interaction)

        # Send log message
        await send_timeout_log(interaction, user, duration_delta, reason, log_channel)

"""
Timeout functionality module - core logic separated from command interface.
"""
import discord
import datetime
from src.res import R, C
from src.utils import create_embed, get_timeout_log_channel, handle_error, logger, error_embed, parse_duration


async def send_timeout_log(interaction: discord.Interaction, user: discord.Member, duration_delta: datetime.timedelta, reason: str | None, log_channel: discord.TextChannel):
    """Sends a log message to the configured timeout log channel."""
    embed = discord.Embed(
        title=R.timeout_log_title,
        color=C.warning_color,
        timestamp=datetime.datetime.now()
    )
    embed.add_field(name=R.timeout_log_user, value=user.mention, inline=True)
    embed.add_field(name=R.timeout_log_moderator,
                    value=interaction.user.mention, inline=True)
    embed.add_field(name=R.timeout_log_duration,
                    value=str(duration_delta), inline=True)
    if reason:
        embed.add_field(name=R.timeout_log_reason,
                        value=reason, inline=False)
    embed.set_thumbnail(url=user.display_avatar.url)

    await log_channel.send(embed=embed)


async def timeout_user(interaction: discord.Interaction, user: discord.Member, duration: str, reason: str = None):
    """
    Timeout a user for a specified duration.
    Args:
        interaction (discord.Interaction): The interaction context.
        user (discord.Member): The user to timeout.
        duration (str): Duration string (e.g., "30s", "2m", "1h").
        reason (str): Optional reason for the timeout.
    """
    await interaction.response.defer(ephemeral=True)

    duration_seconds, err = parse_duration(duration)
    if err:
        await handle_error(interaction, err)
        return
    duration_delta = datetime.timedelta(seconds=duration_seconds)

    if duration_seconds > C.timeout_max_duration:
        await interaction.followup.send(embed=error_embed(R.timeout_duration_too_long), ephemeral=True)
        logger.info(
            f"{interaction.user.name} tried to timeout {user.name} for too long", interaction)
        return

    if user == interaction.user:
        await interaction.followup.send(embed=error_embed(R.timeout_cant_timeout_self), ephemeral=True)
        logger.info(
            f"{interaction.user.name} tried to timeout themselves", interaction)
        return

    if user == interaction.client.user:
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

"""
String resources and constants for the Discord bot, supporting localization and configuration.
"""
# String resources

from dataclasses import dataclass
import discord


@dataclass
class Constants:
    """
    Constants for the bot, such as category names, role names, and colors.
    """

    @dataclass
    class DBKey:
        ticket_category: str = "ticket_category"
        transcript_category: str = "transcript_category"
        mod_roles: str = "mod_role_ids"
        log_channel: str = "log_channel_id"
        locale: str = "lang"
        timeout_log_channel: str = "timeout_log_channel_id"
        welcome_channel_id: str = "welcome_channel_id"

    support_role_name: str = "Support"

    # Key for the timeout log channel in DB
    db_file: str = "db/tickets.db"
    db_schema_file: str = "db/schema.sql"

    embed_desc_max_length: int = 4096  # Max length for embed descriptions
    max_embeds: int = 10  # Max number of embeds per message
    embed_total_max_length: int = 6000  # Max total length for all embeds in a message

    bot_name = "BotControl"
    support_guild_invite_link: str = "https://discord.gg/mD4EQFCC8s"

    cat_application: str = "application"
    cat_report: str = "report"
    cat_support: str = "support"

    # Ticket closing
    ticket_close_time: int = 12  # Hours after which noch fragen-tickets are closed

    # Giveaway settings
    giveaway_check_interval: int = 30  # Seconds between giveaway checks
    giveaway_reaction: str = "🎉"
    application_ban_check_interval: int = 30

    # Embed colors
    embed_color: discord.Color = discord.Color.blue()
    success_color: discord.Color = discord.Color.green()
    error_color: discord.Color = discord.Color.red()
    warning_color: discord.Color = discord.Color.orange()

    giveaway_max_duration: int = 30 * 86400
    giveaway_min_duration: int = 10

    timeout_max_duration: int = 28 * 86400  # Max duration for timeouts in seconds


# Convenient alias
C = Constants

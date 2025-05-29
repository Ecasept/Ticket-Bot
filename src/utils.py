"""
Utility functions and constants for the Discord bot, including role/category helpers and environment loading.
"""
import datetime
import discord
import dotenv
from src.log import Logger
from src.error import Error, We, Ce
from src.res import C, R
import os
from typing import Tuple, Optional, List

dotenv.load_dotenv()

logger = Logger("bot.log")
TOKEN = os.getenv("DISCORD_TOKEN")


def format_date(date: datetime.datetime) -> str:
    """
    Format a datetime object into a string.
    Args:
        date (datetime.datetime): The datetime object to format.
    Returns:
        str: The formatted date string.
    """
    return date.strftime("%d.%m.%Y %H:%M:%S")


def get_mod_roles(guild: discord.Guild) -> Tuple[Optional[List[discord.Role]], Optional[Error]]:
    """
    Retrieve the list of moderator roles for the guild from the database.
    Args:
        guild (discord.Guild): The Discord guild.
    Returns:
        Tuple[Optional[List[discord.Role]], Optional[Error]]: A tuple containing the list of moderator roles (or None) and an error (or None).
    """
    from src.database import db
    mod_role_ids = db.get_constant(C.mod_roles, guild.id)
    if mod_role_ids is None:
        return None, We(R.setup_no_modroles)
    try:
        role_ids = [int(rid) for rid in mod_role_ids.split(",") if rid]
    except ValueError:
        return None, Ce(R.setup_modroles_invalid)
    if not role_ids:
        return None, We(R.setup_no_modroles)
    roles = [guild.get_role(rid) for rid in role_ids]
    if any(role is None for role in roles):
        return None, We(R.setup_modroles_not_found)
    return roles, None


def is_mod_or_admin(user: discord.Member) -> Tuple[Optional[bool], Optional[Error]]:
    """
    Check if the user has a moderator or administrator role.
    Args:
        user (discord.Member): The Discord member to check.
    Returns:
        Tuple[Optional[bool], Optional[Error]]: True if the user has a moderator or administrator role, False otherwise. Returns (None, error) if an error occurs.
    """
    mod_roles, err = get_mod_roles(user.guild)
    if err:
        return None, err
    return any(role.permissions.administrator for role in user.roles) or any(role in mod_roles for role in user.roles), None


def get_member(guild: discord.Guild, user_id: str) -> Tuple[Optional[discord.Member], Optional[Error]]:
    """
    Get a member from the guild by user ID.
    Args:
        guild (discord.Guild): The Discord guild.
        user_id (str): The user ID to search for.
    Returns:
        Tuple[Optional[discord.Member], Optional[Error]]: A tuple of (member, error). If the member is found, returns (member, None). Otherwise returns (None, error) indicating why it failed.
    """
    try:
        id_int = int(user_id)
    except ValueError:
        return None, Ce(R.user_id_invalid)
    member = guild.get_member(id_int)
    if member is None:
        return None, We(R.user_not_found)
    return member, None


async def get_ticket_category(guild: discord.Guild) -> Tuple[Optional[discord.CategoryChannel], Optional[Error]]:
    """
    Get the ticket category where tickets are created.
    Args:
        guild (discord.Guild): The Discord guild to search in.
    Returns:
        Tuple[Optional[discord.CategoryChannel], Optional[Error]]: A tuple of (category, error). If the category is configured and found, returns (category, None). Otherwise returns (None, error) indicating why it failed.
    """
    from src.database import db
    category_id = db.get_constant(C.ticket_category, guild.id)
    if category_id is None:
        return None, We(R.setup_no_ticket_category)
    category = guild.get_channel(int(category_id))
    if not isinstance(category, discord.CategoryChannel):
        return None, We(R.setup_ticket_category_not_found)
    return category, None


async def get_transcript_category(guild: discord.Guild) -> Tuple[Optional[discord.CategoryChannel], Optional[Error]]:
    """
    Return the transcript category for closed tickets.
    Args:
        guild (discord.Guild): The Discord guild to search in.
    Returns:
        Tuple[Optional[discord.CategoryChannel], Optional[Error]]: The transcript category and an error if not found.
    """
    from src.database import db
    category_id = db.get_constant(C.transcript_category, guild.id)
    if category_id is None:
        return None, We(R.setup_no_transcript_category)
    category = guild.get_channel(int(category_id))
    if category is None:
        return None, We(R.setup_transcript_category_not_found)
    return category, None


async def get_log_channel(guild: discord.Guild) -> Tuple[Optional[discord.TextChannel], Optional[Error]]:
    """
    Return the log channel for team actions.
    Args:
        guild (discord.Guild): The Discord guild to search in.
    Returns:
        Tuple[Optional[discord.TextChannel], Optional[Error]]: The log channel and an error if not found.
    """
    from src.database import db
    channel_id = db.get_constant(C.log_channel, guild.id)
    if channel_id is None:
        return None, We(R.setup_no_logchannel)
    channel = guild.get_channel(int(channel_id))
    if not isinstance(channel, discord.TextChannel):
        return None, We(R.setup_logchannel_not_found)
    return channel, None


def error_embed(msg: str, title: Optional[str] = None) -> discord.Embed:
    """
    Create an error embed with a standardized title and color.
    Args:
        msg (str): The error message.
        title (str, optional): The title of the error embed. Defaults to R.error_title.
    Returns:
        discord.Embed: The created error embed.
    """
    return create_embed(msg, color=C.error_color, title=title or R.error_title)


def create_embed(message: str, color: discord.Color = C.embed_color, title: Optional[str] = None) -> discord.Embed:
    """
    Create a Discord embed.
    Args:
        message (str): The main message for the embed.
        color (discord.Color, optional): The color of the embed. Defaults to C.embed_color.
        title (str, optional): The title of the embed. Defaults to None.
    Returns:
        discord.Embed: The created embed.
    """
    embed = discord.Embed(
        title=title,
        description=message,
        color=color
    )
    return embed


def error_to_embed(err: Error) -> discord.Embed:
    """
    Convert an Error object to a Discord embed.
    Args:
        err (Error): The error object containing the message and title.
    Returns:
        discord.Embed: The created embed with the error details.
    """
    return error_embed(err.message, title=err.title)


async def handle_error(interaction: discord.Interaction, err: Error):
    """
    Handle errors by sending an error embed to the interaction.
    Args:
        interaction (discord.Interaction): The interaction context.
        err (Error): The error object to display.
    """
    embed = error_to_embed(err)
    await interaction.respond(embed=embed, ephemeral=True)
    logger.error(err, interaction)


async def verify_mod_or_admin(interaction: discord.Interaction, no_perms_err: Error) -> bool:
    """
    Verify if the user has moderator or administrator permissions.
    Args:
        interaction (discord.Interaction): The interaction context.
        no_permission_msg (str): The message to send if the user does not have permission.
    Returns:
        bool: True if the user has permission, False otherwise.
        Any kind of error handling (logging, sending messages) will be done within this function,
        so if the function returns False, there is no need to take further action.
    """
    has_permission, err = is_mod_or_admin(interaction.user)
    if err:
        await handle_error(interaction, err)
        return False
    if not has_permission:
        await handle_error(interaction, no_perms_err)
        return False
    return True

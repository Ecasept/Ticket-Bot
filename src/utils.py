"""
Utility functions and constants for the Discord bot, including role/category helpers and environment loading.
"""
import datetime
import discord
import dotenv
import src.res as res
import src.log as log
import os
from typing import Tuple, Optional, List

dotenv.load_dotenv()

logger = log.Logger("bot.log")
TOKEN = os.getenv("DISCORD_TOKEN")

R = res.get_resources("de")
C = res.Constants


def format_date(date: datetime.datetime) -> str:
    """
    Format a datetime object into a string.
    Args:
        date (datetime.datetime): The datetime object to format.
    Returns:
        str: The formatted date string.
    """
    return date.strftime("%d.%m.%Y %H:%M:%S")


def get_mod_roles(guild: discord.Guild) -> Tuple[Optional[List[discord.Role]], Optional[str]]:
    """
    Retrieve the list of moderator roles for the guild from the database.
    Args:
        guild (discord.Guild): The Discord guild.
    Returns:
        Tuple[Optional[List[discord.Role]], Optional[str]]: A tuple containing the list of moderator roles (or None) and an error message (or None).
    """
    from src.database import db
    mod_role_ids = db.get_constant(C.mod_roles)
    if mod_role_ids is None:
        return None, R.setup_no_modroles
    try:
        role_ids = [int(rid) for rid in mod_role_ids.split(",") if rid]
    except ValueError:
        return None, R.setup_modroles_invalid
    if not role_ids:
        return None, R.setup_no_modroles
    roles = [guild.get_role(rid) for rid in role_ids]
    if any(role is None for role in roles):
        return None, R.setup_modroles_not_found
    return roles, None


def is_mod_or_admin(user: discord.Member) -> Tuple[Optional[bool], Optional[str]]:
    """
    Check if the user has a moderator or administrator role.
    Args:
        user (discord.Member): The Discord member to check.
    Returns:
        Tuple[Optional[bool], Optional[str]]: True if the user has a moderator or administrator role, False otherwise. Returns (None, error) if an error occurs.
    """
    mod_roles, err = get_mod_roles(user.guild)
    if err:
        return None, err
    return any(role.permissions.administrator for role in user.roles) or any(role in mod_roles for role in user.roles), None


def get_member(guild: discord.Guild, user_id: str) -> Tuple[Optional[discord.Member], Optional[str]]:
    """
    Get a member from the guild by user ID.
    Args:
        guild (discord.Guild): The Discord guild.
        user_id (str): The user ID to search for.
    Returns:
        Tuple[Optional[discord.Member], Optional[str]]: A tuple of (member, error_message). If the member is found, returns (member, None). Otherwise returns (None, error_message) indicating why it failed.
    """
    try:
        id_int = int(user_id)
    except ValueError:
        return None, R.user_id_invalid
    member = guild.get_member(id_int)
    if member is None:
        return None, R.user_not_found
    return member, None


async def get_ticket_category(guild: discord.Guild) -> Tuple[Optional[discord.CategoryChannel], Optional[str]]:
    """
    Get the ticket category where tickets are created.
    Args:
        guild (discord.Guild): The Discord guild to search in.
    Returns:
        Tuple[Optional[discord.CategoryChannel], Optional[str]]: A tuple of (category, error_message). If the category is configured and found, returns (category, None). Otherwise returns (None, error_message) indicating why it failed.
    """
    from src.database import db
    category_id = db.get_constant(C.ticket_category)
    if category_id is None:
        return None, R.setup_no_ticket_category
    category = guild.get_channel(int(category_id))
    if not isinstance(category, discord.CategoryChannel):
        return None, R.setup_ticket_category_not_found
    return category, None


async def get_transcript_category(guild: discord.Guild) -> Tuple[Optional[discord.CategoryChannel], Optional[str]]:
    """
    Return the transcript category for closed tickets.
    Args:
        guild (discord.Guild): The Discord guild to search in.
    Returns:
        Tuple[Optional[discord.CategoryChannel], Optional[str]]: The transcript category and an error message if not found.
    """
    from src.database import db
    category_id = db.get_constant(C.transcript_category)
    if category_id is None:
        return None, R.setup_no_transcript_category
    category = guild.get_channel(int(category_id))
    if category is None:
        return None, R.setup_transcript_category_not_found
    return category, None


async def get_log_channel(guild: discord.Guild) -> Tuple[Optional[discord.TextChannel], Optional[str]]:
    """
    Return the log channel for team actions.
    Args:
        guild (discord.Guild): The Discord guild to search in.
    Returns:
        Tuple[Optional[discord.TextChannel], Optional[str]]: The log channel and an error message if not found.
    """
    from src.database import db
    channel_id = db.get_constant(C.log_channel)
    if channel_id is None:
        return None, R.setup_no_logchannel
    channel = guild.get_channel(int(channel_id))
    if not isinstance(channel, discord.TextChannel):
        return None, R.setup_logchannel_not_found
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

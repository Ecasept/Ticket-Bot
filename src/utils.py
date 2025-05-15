"""
Utility functions and constants for the Discord bot, including role/category helpers and environment loading.
"""
import discord
import dotenv
import src.res as res
import src.log as log
import os

dotenv.load_dotenv()

logger = log.Logger("bot.log")
TOKEN = os.getenv("DISCORD_TOKEN")


def get_support_role(guild: discord.Guild) -> discord.Role:
    """
    Return the role that manages tickets in the server.
    Args:
        guild (discord.Guild): The Discord guild.
    Returns:
        discord.Role: The support role.
    """
    return discord.utils.get(guild.roles, name=C.support_role_name)


async def get_support_category(guild: discord.Guild):
    """
    Return the category that contains the ticket channels. If it doesn't exist, create it.
    Args:
        guild (discord.Guild): The Discord guild.
    Returns:
        discord.CategoryChannel: The support category.
    """
    category = discord.utils.get(
        guild.categories, name=C.support_category_name)

    if category is None:
        logger.info(
            "utils", "Creating support category for server %s", guild.name)
        category = await guild.create_category(C.support_category_name)
        category.set_permissions(
            guild.default_role, read_messages=False)
        category.set_permissions(guild.me, read_messages=True)
        category.set_permissions(get_support_role(guild), read_messages=True)
    return category


async def get_transcript_category(guild: discord.Guild):
    """
    Return the transcript category for closed tickets. If it doesn't exist, create it.
    Args:
        guild (discord.Guild): The Discord guild.
    Returns:
        discord.CategoryChannel: The transcript category.
    """
    category = discord.utils.get(
        guild.categories, name=C.transcript_category_name)
    if category is None:
        logger.info(
            "utils", "Creating transcript category for server %s", guild.name)
        category = await guild.create_category(C.transcript_category_name)
        category.set_permissions(
            guild.default_role, read_messages=False)
        category.set_permissions(guild.me, read_messages=True)
        category.set_permissions(get_support_role(guild), read_messages=True)
    return category


R = res.get_resources("de")
C = res.Constants()

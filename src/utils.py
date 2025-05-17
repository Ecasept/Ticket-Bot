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


def error_embed(msg: str) -> discord.Embed:
    """
    Create an error message embed.
    Args:
        msg (str): The error message.
    Returns:
        discord.Embed: The error message embed.
    """
    embed = discord.Embed(
        description=msg,
        color=discord.Color.red()
    )
    return embed


R = res.get_resources("de")
C = res.Constants()


async def ensure_existence(ticket: dict, interaction: discord.Interaction) -> bool:
    """
    Ensure the ticket exists in the database. Sends an error message if not.
    Args:
        ticket (dict): The ticket data.
        interaction (discord.Interaction): The interaction context.
    Returns:
        bool: True if the ticket exists, False otherwise.
    """
    if ticket is None:
        await interaction.response.send_message(
            embed=error_embed(R.ticket_not_found),
            ephemeral=True
        )
        return False
    return True


async def ensure_assignee(assignee_id: str, interaction: discord.Interaction, msg: str) -> bool:
    """
    Ensure the user has permission to perform an action on the ticket.
    This means that the user is either the assignee (if one is set) or has the support role (if no assignee is set).
    Args:
        assignee_id (str): The ID of the user assigned to the ticket, or None if no one is assigned.
        interaction (discord.Interaction): The interaction context.
        msg (str): The error message if permission is denied.
    Returns:
        bool: True if the user has permission, False otherwise.
    """
    if assignee_id is not None and assignee_id != str(interaction.user.id):
        await interaction.response.send_message(
            embed=error_embed(msg),
            ephemeral=True
        )
        return False
    if assignee_id is None and get_support_role(interaction.guild) not in interaction.user.roles:
        await interaction.response.send_message(
            embed=error_embed(msg),
            ephemeral=True
        )
        return False
    return True

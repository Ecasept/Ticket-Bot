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


class CategoryError(Exception):
    """Custom exception for category-related errors."""
    pass


def get_support_role(guild: discord.Guild) -> discord.Role:
    """
    Return the role that manages tickets in the server.
    Args:
        guild (discord.Guild): The Discord guild.
    Returns:
        discord.Role: The support role.
    """
    return discord.utils.get(guild.roles, name=C.support_role_name)


async def get_ticket_category(interaction: discord.Interaction) -> discord.CategoryChannel:
    """
    Return the ticket category where tickets are contained. If it doesn't exist, send an error message and raise an exception.
    Args:
        interaction (discord.Interaction): The interaction context.
    Returns:
        discord.CategoryChannel: The support category.
    Raises:
        CategoryError: If the category is not set or not found.
    """
    from src.database import db
    category_id = db.get_constant(C.ticket_category)
    if category_id is None:
        # No category set
        msg = R.setup_no_ticket_category
        await interaction.followup.send(
            embed=error_embed(msg),
            ephemeral=True
        )
        raise CategoryError(msg)
    category = interaction.guild.get_channel(int(category_id))
    if category is None:
        # Category not found
        msg = R.setup_ticket_category_not_found
        await interaction.followup.send(
            embed=error_embed(msg),
            ephemeral=True
        )
        raise CategoryError(msg)
    return category


async def get_transcript_category(interaction: discord.Interaction) -> discord.CategoryChannel:
    """
    Return the transcript category for closed tickets. If it doesn't exist, send an error message and raise an exception.
    Args:
        interaction (discord.Interaction): The interaction context.
    Returns:
        discord.CategoryChannel: The transcript category.
    Raises:
        CategoryError: If the category is not set or not found.
    """
    from src.database import db
    category_id = db.get_constant(
        C.transcript_category)
    if category_id is None:
        # No category set
        msg = R.setup_no_transcript_category
        await interaction.followup.send(
            embed=error_embed(msg),
            ephemeral=True
        )
        raise CategoryError(msg)
    category = interaction.guild.get_channel(int(category_id))
    if category is None:
        # Category not found
        msg = R.setup_transcript_category_not_found
        await interaction.followup.send(
            embed=error_embed(msg),
            ephemeral=True
        )
        raise CategoryError(msg)
    return category


R = res.get_resources("de")
C = res.Constants()


def error_embed(msg: str, title: str = None) -> discord.Embed:
    """
    Create an error embed with a standardized title and color.
    Args:
        msg (str): The error message.
        title (str, optional): The title of the error embed. Defaults to R.error_title.
    Returns:
        discord.Embed: The created error embed.
    """
    return create_embed(msg, color=C.error_color, title=title or R.error_title)


def create_embed(message: str, color: discord.Color = C.embed_color, title: str = None) -> discord.Embed:
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


async def ensure_existence(ticket: dict, interaction: discord.Interaction) -> bool:
    """
    Ensure a ticket exists in the database. If not, send an error message and return False.
    Args:
        ticket (dict): The ticket to check.
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

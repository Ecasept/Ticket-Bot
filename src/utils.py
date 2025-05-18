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


async def get_ticket_category(interaction: discord.Interaction) -> discord.CategoryChannel | None:
    """
    Return the ticket category where tickets are contained. If it doesn't exist, send an error message and return `None`.
    No action needs to be taken if `None` is returned, as the user is already informed. The command can be cancelled.
    Args:
        interaction (discord.Interaction): The interaction context.
    Returns:
        discord.CategoryChannel: The support category, or `None` if it doesn't exist.
    """
    from src.database import db
    category_id = db.get_constant(C.ticket_category)
    if category_id is None:
        # No category set
        await interaction.response.send_message(
            embed=error_embed(R.setup_no_ticket_category),
            ephemeral=True
        )
        return None
    category = interaction.guild.get_channel(int(category_id))
    if category is None:
        # Category not found
        await interaction.response.send_message(
            embed=error_embed(R.setup_ticket_category_not_found),
            ephemeral=True
        )
        return None
    return category


async def get_transcript_category(interaction: discord.Interaction) -> discord.CategoryChannel | None:
    """
    Return the transcript category for closed tickets. If it doesn't exist, send an error message and return `None`.
    No action needs to be taken if `None` is returned, as the user is already informed. The command can be cancelled.
    Args:
        interaction (discord.Interaction): The interaction context.
    Returns:
        discord.CategoryChannel: The transcript category, or `None` if it doesn't exist.
    """
    from src.database import db
    category_id = db.get_constant(
        C.transcript_category)
    if category_id is None:
        # No category set
        await interaction.response.send_message(
            embed=error_embed(R.setup_no_transcript_category),
            ephemeral=True
        )
        return None
    category = interaction.guild.get_channel(int(category_id))
    if category is None:
        # Category not found
        await interaction.response.send_message(
            embed=error_embed(R.setup_transcript_category_not_found),
            ephemeral=True
        )
        return None
    return category


def error_embed(msg: str) -> discord.Embed:
    """
    Create an error message embed.
    Args:
        msg (str): The error message.
    Returns:
        discord.Embed: The error message embed.
    """
    return create_embed(msg, discord.Color.red())


R = res.get_resources("de")
C = res.Constants()


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

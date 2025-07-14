"""
Shared utilities and functions for category management.
"""
import discord
from typing import List, Dict, Optional
from src.database.ticket_category import TicketCategory
from src.res import R, C
from src.utils import create_embed
from src.database import db


def get_category_details(category_id: int) -> Optional[dict]:
    """
    Get detailed information about a category.

    Args:
        category_id (int): The category ID.

    Returns:
        Dict: Category details including roles and questions, or None if not found.
    """
    category = db.tc.get_category(category_id)
    if not category:
        return None

    role_ids = db.tc.get_role_permissions(category_id)
    questions = db.tc.get_questions(category_id)

    return {
        'category': category,
        'role_ids': role_ids,
        'questions': questions
    }


def create_category_embed(category, role_ids: List[int] = None, questions: List = None, guild: discord.Guild = None) -> discord.Embed:
    """
    Create an embed showing category information.

    Args:
        category: The category object.
        role_ids (List[int]): List of role IDs with permission.
        questions (List): List of question tuples.
        guild (discord.Guild): Guild object for role mentions.

    Returns:
        discord.Embed: The formatted embed.
    """
    embed = discord.Embed(
        title=f"{category.emoji} {category.name}",
        description=category.description,
        color=C.embed_color
    )

    embed.add_field(name="ID", value=str(category.id), inline=True)

    # Role permissions
    if role_ids and guild:
        roles = [guild.get_role(rid) for rid in role_ids]
        roles = [r for r in roles if r]  # Filter out None roles
        if roles:
            role_text = ", ".join([r.mention for r in roles])
            embed.add_field(name="Berechtigung", value=role_text, inline=False)
        else:
            embed.add_field(name="Berechtigung",
                            value="Alle Benutzer", inline=False)
    else:
        embed.add_field(name="Berechtigung",
                        value="Alle Benutzer", inline=False)

    # Questions
    if questions:
        question_list = "\n".join(
            [f"{i+1}. {q[1]}" for i, q in enumerate(questions)])
        embed.add_field(
            name=f"Fragen ({len(questions)})",
            value=question_list[:1024] if len(
                question_list) <= 1024 else question_list[:1021] + "...",
            inline=False
        )
    else:
        embed.add_field(
            name="Fragen", value="Keine Fragen konfiguriert", inline=False)

    return embed


class CategorySelectView(discord.ui.View):
    """Base view for selecting a category from a dropdown."""

    def __init__(self, guild: discord.Guild, categories: list[TicketCategory], placeholder: str = "Kategorie wählen..."):
        super().__init__(timeout=300)
        self.categories = categories

        # Create select menu with categories
        options = []
        for cat in categories[:25]:  # Discord limit

            emoji = cat.emoji.strip()
            if emoji.startswith(":") and emoji.endswith(":"):
                emoji = discord.utils.get(guild.emojis, name=emoji[1:-1])
            else:
                emoji = discord.PartialEmoji.from_str(emoji)

            options.append(discord.SelectOption(
                label=cat.name,
                value=str(cat.id),
                description=cat.description[:100] if cat.description else "Keine Beschreibung",
                emoji=emoji
            ))
        if options:
            select = discord.ui.Select(
                placeholder=placeholder,
                options=options
            )
            select.callback = self.select_callback
            self.add_item(select)

    async def select_callback(self, interaction: discord.Interaction):
        """Override this method in subclasses."""
        pass

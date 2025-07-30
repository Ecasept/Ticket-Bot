"""
Category removal functionality.
Handles deletion of ticket categories with confirmation dialogs.
"""
from typing import override
import discord
from src.res import R
from src.res.utils import late, button, LateView
from src.database.ticket_category import TicketCategory
from src.utils import create_embed, handle_error
from src.constants import C
from src.database import db
from src.error import Ce, We
from .shared import get_category_details, CategorySelectView
from src.utils import logger


async def perform_category_removal(category, interaction: discord.Interaction) -> bool:
    """
    Perform the actual category removal with all checks.

    Args:
        category: The category object to remove.
        interaction: The Discord interaction object.

    Returns:
        bool: True if successful, False otherwise.
    """
    # Check if category can be removed
    can_remove, reason = can_remove_category(category.id)

    if not can_remove:
        await handle_error(interaction, We(reason))

    db.tc.delete_category(category.id)


class CategoryRemoveConfirmView(LateView):
    """Confirmation view for removing a category."""

    def __init__(self, category):
        super().__init__(timeout=60)
        self.category = category

    @late(lambda: button(label=R.category_yes_delete, style=discord.ButtonStyle.danger, emoji="🗑️"))
    async def confirm_remove(self, button: discord.ui.Button, interaction: discord.Interaction):
        """Confirm category removal."""

        # Use the extracted removal function
        await perform_category_removal(self.category, interaction)

        embed = create_embed(
            R.feature.category.remove.delete_success % self.category.name,
            color=C.success_color,
            title=R.feature.category.remove.delete_success_title
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(
            f"Category '{self.category.name}'", interaction)

    @late(lambda: button(label=R.category_cancel, style=discord.ButtonStyle.secondary, emoji="❌"))
    async def cancel_remove(self, button: discord.ui.Button, interaction: discord.Interaction):
        """Cancel category removal."""
        embed = create_embed(
            R.feature.category.remove.delete_cancelled,
            color=C.embed_color,
            title=R.feature.category.remove.delete_cancelled_title
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


class CategoryRemoveSelectView(CategorySelectView):
    """Select view for choosing a category to remove."""

    def __init__(self, interaction: discord.Interaction, categories: list[TicketCategory]):
        super().__init__(interaction.guild, categories,
                         placeholder=R.category_select_placeholder)

    @override
    async def select_callback(self, interaction: discord.Interaction):
        """Handle category selection for removal."""
        await super().select_callback(interaction)
        selected_category_id = int(self.children[0].values[0])
        category = db.tc.get_category(selected_category_id)

        if not category:
            await handle_error(interaction, Ce(R.feature.category.remove.not_found))
            return

        # Create confirmation embed
        embed = create_embed(
            R.feature.category.remove.confirm_embed_desc % (
                category.name,
                category.emoji,
                category.description or R.feature.category.remove.no_description
            ),
            color=C.error_color,
            title=R.feature.category.remove.confirm_embed_title % category.name
        )

        confirm_view = CategoryRemoveConfirmView(category)
        await interaction.response.send_message(embed=embed, view=confirm_view, ephemeral=True)


async def handle_remove_category(interaction: discord.Interaction) -> None:
    """Handle showing category removal selection."""
    categories = db.tc.get_categories_for_guild(interaction.guild.id)

    if not categories:
        embed = create_embed(
            R.feature.category.remove.no_categories_found,
            color=C.warning_color,
            title=R.feature.category.remove.no_categories_found_title
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    view = CategoryRemoveSelectView(interaction, categories)
    embed = create_embed(
        R.feature.category.remove.select_prompt,
        title=R.feature.category.remove.select_prompt_title
    )

    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


def can_remove_category(category_id: int) -> tuple[bool, str]:
    """
    Check if a category can be removed.

    Args:
        category_id (int): The ID of the category to check.

    Returns:
        tuple[bool, str]: (can_remove, reason_if_not)
    """
    # Check if category exists
    category = db.tc.get_category(category_id)
    if not category:
        return False, R.feature.category.remove.not_found

    # Check for active tickets
    ticket_count = db.tc.get_ticket_count(category_id)
    if ticket_count > 0:
        return False, R.feature.category.remove.still_active_tickets % ticket_count

    return True, ""

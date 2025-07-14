"""
Category removal functionality.
Handles deletion of ticket categories with confirmation dialogs.
"""
import discord
from src.database.ticket_category import TicketCategory
from src.utils import create_embed, handle_error
from src.res import C
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


class CategoryRemoveConfirmView(discord.ui.View):
    """Confirmation view for removing a category."""

    def __init__(self, category):
        super().__init__(timeout=60)
        self.category = category

    @discord.ui.button(label="Ja, löschen", style=discord.ButtonStyle.danger, emoji="🗑️")
    async def confirm_remove(self, button: discord.ui.Button, interaction: discord.Interaction):
        """Confirm category removal."""

        # Use the extracted removal function
        await perform_category_removal(self.category, interaction)

        embed = create_embed(
            f"Kategorie '{self.category.name}' wurde erfolgreich gelöscht.",
            color=C.success_color,
            title="Kategorie gelöscht"
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(
            f"Category '{self.category.name}'", interaction)

    @discord.ui.button(label="Abbrechen", style=discord.ButtonStyle.secondary, emoji="❌")
    async def cancel_remove(self, button: discord.ui.Button, interaction: discord.Interaction):
        """Cancel category removal."""
        embed = create_embed(
            "Kategorie-Löschung abgebrochen.",
            color=C.embed_color,
            title="Abgebrochen"
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


class CategoryRemoveSelectView(CategorySelectView):
    """Select view for choosing a category to remove."""

    def __init__(self, interaction: discord.Interaction, categories: list[TicketCategory]):
        super().__init__(interaction.guild, categories,
                         placeholder="Wähle eine Kategorie zum Löschen...")

    async def select_callback(self, interaction: discord.Interaction):
        """Handle category selection for removal."""
        selected_category_id = int(self.children[0].values[0])
        category = db.tc.get_category(selected_category_id)

        if not category:
            await handle_error(interaction, Ce("Kategorie nicht gefunden"))
            return

        # Create confirmation embed
        embed = create_embed(
            f"**Name:** {category.name}\n"
            f"**Emoji:** {category.emoji}\n"
            f"**Beschreibung:** {category.description or 'Keine Beschreibung'}\n\n"
            f"**⚠️ Warnung:** Diese Aktion kann nicht rückgängig gemacht werden!\n"
            f"Alle Fragen und Rollen-Zuweisungen werden ebenfalls gelöscht.",
            color=C.error_color,
            title=f"Kategorie '{category.name}' löschen?"
        )

        confirm_view = CategoryRemoveConfirmView(category)
        await interaction.response.send_message(embed=embed, view=confirm_view, ephemeral=True)


async def handle_remove_category(interaction: discord.Interaction) -> None:
    """Handle showing category removal selection."""
    categories = db.tc.get_categories_for_guild(interaction.guild.id)

    if not categories:
        embed = create_embed(
            "Keine Kategorien gefunden. Verwende '/category create' um eine zu erstellen.",
            color=C.warning_color,
            title="Keine Kategorien"
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    view = CategoryRemoveSelectView(interaction, categories)
    embed = create_embed(
        "Wähle eine Kategorie zum Löschen:",
        title="Kategorie löschen"
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
        return False, "Kategorie nicht gefunden"

    # Check for active tickets
    ticket_count = db.tc.get_ticket_count(category_id)
    if ticket_count > 0:
        return False, f"Kategorie hat noch {ticket_count} aktive Tickets"

    return True, ""

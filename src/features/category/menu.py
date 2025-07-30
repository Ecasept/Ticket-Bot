"""
Category menu interface for the ticket system.
Main menu for category management functionality.
"""
import discord
from src.res import R
from src.res.utils import late, button, LateView
from src.constants import C
from src.utils import create_embed, handle_error, logger
from src.database import db
from src.error import Ce, We
from .create import handle_create_category
from .edit import handle_edit_categories
from .remove import handle_remove_category


class CategoryButton(discord.ui.Button):
    """Button for category management in the ticket menu."""

    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.secondary,
            label=R.feature.category.menu.button_label,
            emoji="📂",
            custom_id="category_management"
        )

    async def callback(self, interaction: discord.Interaction):
        """Handle category button click."""
        await R.init(interaction.guild_id)
        # Show category management menu
        view = CategoryManagementView()
        embed = create_embed(
            R.feature.category.menu.description,
            title=R.feature.category.menu.title
        )

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        logger.info(
            f"Category management menu shown to {interaction.user}", interaction)


class CategoryManagementView(LateView):
    """Main view for category management options."""

    def __init__(self):
        super().__init__(timeout=300)

    @late(lambda: button(label=R.category_new, style=discord.ButtonStyle.primary, emoji="➕"))
    async def create_category_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        """Handle create category button."""
        # Use shared handler that includes modal creation
        await handle_create_category(interaction)

    @late(lambda: button(label=R.category_edit, style=discord.ButtonStyle.secondary, emoji="✏️"))
    async def edit_category_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        """Handle edit category button."""
        await handle_edit_categories(interaction)

    @late(lambda: button(label=R.category_delete, style=discord.ButtonStyle.danger, emoji="🗑️"))
    async def remove_category_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        """Handle remove category button."""
        await handle_remove_category(interaction)

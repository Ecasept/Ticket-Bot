"""
Role permission management for ticket categories.
Handles role-based access control for categories.
"""
import discord
from src.res import R, C
from src.utils import create_embed, handle_error, logger
from src.database import db
from src.error import Ce


class CategoryRoleEditView(discord.ui.View):
    """View for editing role permissions for a category."""

    def __init__(self, category):
        super().__init__(timeout=300)
        self.category = category
        self.selected_roles = []

    @discord.ui.role_select(
        placeholder="Rollen auswählen (leer = alle Benutzer)...",
        min_values=0,
        max_values=25
    )
    async def role_select(self, select: discord.ui.Select, interaction: discord.Interaction):
        self.selected_roles = select.values
        await interaction.response.defer()

    @discord.ui.button(label="Speichern", style=discord.ButtonStyle.success, emoji="💾")
    async def save_roles(self, button: discord.ui.Button, interaction: discord.Interaction):
        role_ids = [role.id for role in self.selected_roles]
        db.tc.set_category_roles(self.category.id, role_ids)

        if role_ids:
            role_mentions = ", ".join(
                [role.mention for role in self.selected_roles])
            message = f"Berechtigung für '{self.category.name}' auf folgende Rollen beschränkt: {role_mentions}"
        else:
            message = f"Kategorie '{self.category.name}' ist jetzt für alle Benutzer verfügbar"

        embed = create_embed(
            message,
            color=C.success_color,
            title="Berechtigung aktualisiert"
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

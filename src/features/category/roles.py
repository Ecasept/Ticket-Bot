"""
Role permission management for ticket categories.
Handles role-based access control for categories.
"""
import discord
from src.constants import C
from src.res import R
from src.res.utils import LateView, button, late, role_select
from src.utils import create_embed, handle_error
from src.database import db
from src.error import Ce


class CategoryRoleEditView(LateView):
    """View for editing role permissions for a category."""

    def __init__(self, category):
        super().__init__(timeout=300)
        self.category = category
        self.selected_roles = []

    @late(lambda: role_select(
        placeholder=R.category_roles_placeholder,
        min_values=0,
        max_values=25
    ))
    async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        roles = select.values
        self.selected_roles = roles
        await interaction.response.defer()

    @late(lambda: button(label=R.category_save, style=discord.ButtonStyle.success, emoji="💾"))
    async def save_roles(self, button: discord.ui.Button, interaction: discord.Interaction):
        role_ids = [role.id for role in self.selected_roles]
        db.tc.set_category_roles(self.category.id, role_ids)

        if role_ids:
            role_mentions = ", ".join(
                [role.mention for role in self.selected_roles])
            message = R.feature.category.roles.permissions_limited % (
                self.category.name, role_mentions)
        else:
            message = R.feature.category.roles.permissions_all_users % self.category.name

        embed = create_embed(
            message,
            color=C.success_color,
            title=R.feature.category.roles.permissions_updated_title
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

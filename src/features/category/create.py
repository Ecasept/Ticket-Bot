"""
Category creation functionality.
Handles creating new ticket categories with modal input.
"""
import discord
from src.res import R
from src.constants import C
from src.utils import create_embed, handle_error, logger
from src.database import db
from src.error import Ce


class CategoryCreateModal(discord.ui.Modal):
    """Modal for creating a new ticket category."""

    def __init__(self):
        super().__init__(title=R.feature.category.create.modal.title)

        self.category_name = discord.ui.InputText(
            label=R.feature.category.create.modal.name_label,
            placeholder=R.feature.category.create.modal.name_placeholder,
            required=True,
            max_length=100
        )

        self.category_emoji = discord.ui.InputText(
            label=R.feature.category.create.modal.emoji_label,
            placeholder=R.feature.category.create.modal.emoji_placeholder,
            required=True,
            max_length=50
        )

        self.category_description = discord.ui.InputText(
            label=R.feature.category.create.modal.description_label,
            placeholder=R.feature.category.create.modal.description_placeholder,
            required=True,
            style=discord.InputTextStyle.long,
            max_length=1000
        )

        self.add_item(self.category_name)
        self.add_item(self.category_emoji)
        self.add_item(self.category_description)

    async def callback(self, interaction: discord.Interaction):
        """Handle the modal submission."""
        await interaction.response.defer()


async def handle_create_category(interaction: discord.Interaction) -> None:
    """Handle category creation with modal input."""
    modal = CategoryCreateModal()
    await interaction.response.send_modal(modal)
    await modal.wait()

    if not (modal.category_name and modal.category_emoji and modal.category_description):
        return  # User cancelled or incomplete data

    category_id = db.tc.create_category(
        name=modal.category_name.value,
        emoji=modal.category_emoji.value,
        description=modal.category_description.value,
        guild_id=interaction.guild.id
    )

    embed = create_embed(
        R.feature.category.create.success_desc % modal.category_name.value,
        color=C.success_color,
        title=R.feature.category.create.success_title
    )
    embed.add_field(name=R.feature.category.create.field_id,
                    value=str(category_id), inline=True)
    embed.add_field(name=R.feature.category.create.field_name,
                    value=modal.category_name.value, inline=True)
    embed.add_field(name=R.feature.category.create.field_emoji,
                    value=modal.category_emoji.value, inline=True)
    embed.add_field(name=R.feature.category.create.field_description,
                    value=modal.category_description.value, inline=False)

    await interaction.followup.send(embed=embed, ephemeral=True)
    logger.info(
        f"Category '{modal.category_name.value}' created with ID {category_id} by {interaction.user}", interaction)

"""
Category editing functionality.
Handles editing existing ticket categories including basic info, roles, and questions.
"""
import discord
from src.database.ticket_category import TicketCategory
from src.res import R, C
from src.utils import create_embed, handle_error, logger
from src.database import db
from src.error import Ce
from .shared import CategorySelectView


class CategoryEditModal(discord.ui.Modal):
    """Modal for editing basic category information."""

    def __init__(self, category: TicketCategory | None):
        super().__init__(title=f"Bearbeite {category.name}")
        self.category = category

        self.category_name = discord.ui.InputText(
            label="Name",
            placeholder="Name der Kategorie",
            required=True,
            value=category.name,
            max_length=100
        )

        self.category_emoji = discord.ui.InputText(
            label="Emoji",
            placeholder="Emoji für die Kategorie",
            required=True,
            value=category.emoji,
            max_length=50
        )

        self.category_description = discord.ui.InputText(
            label="Beschreibung",
            placeholder="Beschreibung der Kategorie",
            required=True,
            value=category.description,
            style=discord.InputTextStyle.long,
            max_length=1000
        )

        self.add_item(self.category_name)
        self.add_item(self.category_emoji)
        self.add_item(self.category_description)

    async def callback(self, interaction: discord.Interaction):
        """Handle the modal submission."""
        await interaction.response.defer()


class CategoryEditSelectView(CategorySelectView):
    """View for selecting a category to edit."""

    def __init__(self, interaction: discord.Interaction, categories: list[TicketCategory]):
        super().__init__(interaction.guild, categories, "Kategorie zum Bearbeiten wählen...")

    async def select_callback(self, interaction: discord.Interaction):
        category_id = int(interaction.data["values"][0])
        category = db.tc.get_category(category_id)

        if not category:
            await interaction.response.send_message("Kategorie nicht gefunden!", ephemeral=True)
            return

        # Show edit options
        view = CategoryEditOptionsView(category)
        embed = create_embed(
            f"Bearbeite Kategorie: {category.emoji} {category.name}",
            title="Kategorie bearbeiten"
        )

        await interaction.response.edit_message(embed=embed, view=view)


class CategoryEditOptionsView(discord.ui.View):
    """View showing edit options for a category."""

    def __init__(self, category):
        super().__init__(timeout=300)
        self.category = category

    @discord.ui.button(label="Name/Emoji/Beschreibung", style=discord.ButtonStyle.primary, emoji="✏️")
    async def edit_basic_info(self, button: discord.ui.Button, interaction: discord.Interaction):
        modal = CategoryEditModal(self.category)
        await interaction.response.send_modal(modal)
        await modal.wait()

        if modal.category_name and modal.category_emoji and modal.category_description:
            db.tc.update_category(
                self.category.id,
                name=modal.category_name.value,
                emoji=modal.category_emoji.value,
                description=modal.category_description.value
            )

            embed = create_embed(
                f"Kategorie '{modal.category_name.value}' erfolgreich aktualisiert!",
                color=C.success_color,
                title="Kategorie aktualisiert"
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

    @discord.ui.button(label="Rollen-Berechtigung", style=discord.ButtonStyle.secondary, emoji="👥")
    async def edit_roles(self, button: discord.ui.Button, interaction: discord.Interaction):
        from .roles import CategoryRoleEditView

        view = CategoryRoleEditView(self.category)
        embed = create_embed(
            f"Berechtigungen für: {self.category.emoji} {self.category.name}",
            title="Rollen-Berechtigung bearbeiten"
        )

        role_ids = db.tc.get_role_permissions(self.category.id)
        if role_ids:
            roles = [interaction.guild.get_role(rid) for rid in role_ids]
            roles = [r for r in roles if r]  # Filter out None roles
            if roles:
                embed.add_field(
                    name="Aktuelle Rollen",
                    value=", ".join([r.mention for r in roles]),
                    inline=False
                )
        else:
            embed.add_field(
                name="Aktuelle Berechtigung",
                value="Alle Benutzer können diese Kategorie verwenden",
                inline=False
            )

        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Fragen", style=discord.ButtonStyle.secondary, emoji="❓")
    async def edit_questions(self, button: discord.ui.Button, interaction: discord.Interaction):
        from .questions import CategoryQuestionEditView

        view = CategoryQuestionEditView(self.category)
        embed = create_embed(
            f"Fragen für: {self.category.emoji} {self.category.name}",
            title="Fragen bearbeiten"
        )

        questions = db.tc.get_questions(self.category.id)
        if questions:
            question_list = "\n".join(
                [f"{i+1}. {q[1]}" for i, q in enumerate(questions)])
            embed.add_field(
                name="Aktuelle Fragen",
                value=question_list[:1024],  # Discord field limit
                inline=False
            )
        else:
            embed.add_field(
                name="Fragen",
                value="Keine Fragen konfiguriert",
                inline=False
            )

        await interaction.response.edit_message(embed=embed, view=view)


async def handle_edit_categories(interaction: discord.Interaction) -> None:
    """Handle showing category edit selection."""
    categories = db.tc.get_categories_for_guild(interaction.guild.id)

    if not categories:
        embed = create_embed(
            "Keine Kategorien gefunden. Verwende '/category create' um eine zu erstellen.",
            color=C.warning_color,
            title="Keine Kategorien"
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    view = CategoryEditSelectView(interaction, categories)
    embed = create_embed(
        "Wähle eine Kategorie zum Bearbeiten:",
        title="Kategorie bearbeiten"
    )

    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    logger.info(
        f"Category edit selection shown to {interaction.user}", interaction)

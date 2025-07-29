"""
Main ticket menu interface that combines all command buttons.
"""
import discord
from src.res import R
from src.utils import logger
from src.features.giveaway.button import GiveawayButton
from src.features.timeout.button import TimeoutButton
from src.features.setup.button import SetupButton
from src.features.category.menu import CategoryButton
from src.constants import C


class TicketMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Persistent view

        # Add all the button components
        self.add_item(GiveawayButton())
        self.add_item(TimeoutButton())
        self.add_item(SetupButton())
        self.add_item(CategoryButton())


def create_ticket_menu_embed():
    """
    Create the embed for the ticket menu.
    Returns:
        discord.Embed: The formatted ticket menu embed.
    """
    embed = discord.Embed(
        title=R.ticket_menu_title,
        description=R.ticket_menu_description,
        color=C.embed_color
    )

    embed.add_field(
        name="🎉 " + R.ticket_menu_giveaway,
        value=R.ticket_menu_giveaway_desc,
        inline=True
    )

    embed.add_field(
        name="⏰ " + R.ticket_menu_timeout,
        value=R.ticket_menu_timeout_desc,
        inline=True
    )

    embed.add_field(
        name="⚙️ " + R.ticket_menu_setup,
        value=R.ticket_menu_setup_desc,
        inline=True
    )

    embed.add_field(
        name="📂 Kategorien",
        value="Verwalte benutzerdefinierte Ticket-Kategorien",
        inline=True
    )

    return embed


async def send_ticket_menu(interaction: discord.Interaction):
    """
    Send the ticket menu embed with buttons.
    Args:
        interaction (discord.Interaction): The interaction context.
    """
    embed = create_ticket_menu_embed()
    view = TicketMenuView()

    await interaction.response.send_message(embed=embed, view=view, ephemeral=False)
    logger.info("Ticket menu sent", interaction)

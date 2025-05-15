import discord

from src.mod_options import ModOptionsMessage
from src.utils import R, get_transcript_category
from src.database import db


class HeaderView(discord.ui.View):
    """
    A view that contains buttons for ticket options.
    """
    view_id: str = "ticket_options"

    def __init__(self):
        super().__init__(timeout=None)

        close_button = discord.ui.Button(
            label=R.close_ticket, style=discord.ButtonStyle.danger, custom_id="close_ticket")
        close_button.callback = self.close_ticket
        self.add_item(close_button)

        mod_options = discord.ui.Button(
            label=R.mod_options, style=discord.ButtonStyle.secondary, custom_id="mod_options")
        mod_options.callback = self.open_mod_options
        self.add_item(mod_options)

    async def close_ticket(self, interaction: discord.Interaction):
        # Change category
        category = await get_transcript_category(interaction.guild)
        await interaction.channel.edit(category=category)

        db.delete_ticket(str(interaction.channel.id))

        await interaction.edit(
            content=R.ticket_closed_msg,
            view=None
        )

    async def open_mod_options(self, interaction: discord.Interaction):
        msg, view = ModOptionsMessage.create(
            interaction,
        )

        await interaction.response.send_message(
            content=msg,
            view=view,
            ephemeral=True
        )

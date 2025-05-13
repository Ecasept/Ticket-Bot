import discord

from ticket import create_ticket_channel, init_ticket_channel
from utils import C, R


class TicketCategorySelection(discord.ui.View):

    @discord.ui.select(
        placeholder=R.ticket_category_placeholder,
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label=R.application, value=C.cat_application, description=R.application_desc),
            discord.SelectOption(
                label=R.report, value=C.cat_report, description=R.report_desc),
        ]
    )
    async def callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        category = select.values[0]

        await interaction.response.defer(ephemeral=True)

        channel = await create_ticket_channel(interaction.guild, interaction.user, category)
        await init_ticket_channel(interaction.guild, interaction.user, channel, category)

        msg = R.ticket_channel_created % channel.mention
        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            content=msg, view=None)

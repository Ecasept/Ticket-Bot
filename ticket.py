import discord

import dynamic
from mod_options import ModOptionsMessage
from utils import C, logger, R, get_support_category, get_support_role, get_transcript_category


def generate_channel_name(user: discord.User, category: str):
    prefix = R.application_prefix if category == C.cat_application else R.report_prefix

    channel_name = f"{prefix}-{user.name}"
    i = 1
    while True:
        channel = discord.utils.get(
            user.guild.text_channels, name=channel_name)
        if channel is None:
            break
        i += 1
        channel_name = f"{prefix}-{user.name}-{i}"
    return channel_name


async def create_ticket_channel(guild: discord.Guild, user: discord.User, category: str):
    support_category = await get_support_category(guild)

    channel_name = generate_channel_name(user, category)
    support_role = get_support_role(guild)

    channel = await guild.create_text_channel(
        name=channel_name,
        category=support_category,
        overwrites={
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            support_role: discord.PermissionOverwrite(read_messages=True),
            user: discord.PermissionOverwrite(read_messages=True)
        }
    )

    logger.info(f"Ticket channel created for {user.name} (ID: {user.id})")
    return channel


async def init_ticket_channel(guild: discord.Guild, user: discord.User, channel: discord.TextChannel, category: str):
    msg, view = TicketOptionsMessage.create(
        user,
        category,
    )
    await channel.send(content=msg, view=view)

    logger.info(
        f"Ticket channel initialized for {user.name} (ID: {user.id})")


class TicketOptionsMessage(dynamic.DynamicPersistentView):
    """
    A view that contains buttons for ticket options.
    """
    view_id: str = "ticket_options"

    def __init__(self, category: str, assigned_id: str, archived: str):
        super().__init__(self.view_id, category, assigned_id, archived)
        self.category = category
        self.assigned_id = assigned_id
        self.archived = archived

        close_button = discord.ui.Button(
            label=R.close_ticket, style=discord.ButtonStyle.danger, custom_id="close_ticket")
        close_button.callback = self.close_ticket
        self.add_item(close_button)

        mod_options = discord.ui.Button(
            label=R.mod_options, style=discord.ButtonStyle.secondary, custom_id="mod_options")
        mod_options.callback = self.open_mod_options
        self.add_item(mod_options)

        # if assigned_id is None:
        #     assign_button = discord.ui.Button(
        #         label=R.assign_ticket, style=discord.ButtonStyle.primary, custom_id="assign_ticket")
        #     assign_button.callback = self.assign_ticket
        #     self.add_item(assign_button)
        # else:
        #     unassign_button = discord.ui.Button(
        #         label=R.unassign_ticket, style=discord.ButtonStyle.primary, custom_id="unassign_ticket")
        #     unassign_button.callback = self.unassign_ticket
        #     self.add_item(unassign_button)

    async def close_ticket(self, interaction: discord.Interaction):
        # Change category
        category = await get_transcript_category(interaction.guild)
        await interaction.channel.edit(category=category)

        await interaction.edit(
            content=R.ticket_closed_msg,
            view=None
        )

    async def open_mod_options(self, interaction: discord.Interaction):
        msg, view = ModOptionsMessage.create(
            interaction,
            self.category,
            self.assigned_id,
            str(interaction.message.id),
            self.archived
        )

        await interaction.response.send_message(
            content=msg,
            view=view,
            ephemeral=True
        )

    @staticmethod
    def create(user: discord.User, category: str, assigned_id: str = "", archived: str = ""):
        msg = R.ticket_options_msg_application if category == C.cat_application else R.ticket_options_msg_report
        msg = msg % user.mention
        view = TicketOptionsMessage(
            category,
            assigned_id,
            archived
        )
        return msg, view

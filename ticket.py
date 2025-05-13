import discord

import dynamic
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
    view = TicketOptionsView(category, "1")

    await channel.send(
        f"Hallo {user.mention}, willkommen in deinem Ticket-Kanal!", view=view
    )
    logger.info(
        f"Ticket channel initialized for {user.name} (ID: {user.id})")


class TicketOptionsView(dynamic.DynamicPersistentView):
    """
    A view that contains buttons for ticket options.
    """
    view_id: str = "ticket_options"

    def __init__(self, category: str, assigned_id: str = "", archived: str = ""):
        super().__init__(self.view_id, category, assigned_id)
        self.category = category
        self.assigned_id = None if assigned_id == "" else int(assigned_id)
        self.archived = False if archived == "" else bool(archived)

        close_button = discord.ui.Button(
            label=R.close_ticket, style=discord.ButtonStyle.danger, custom_id="close_ticket")
        close_button.callback = self.close_ticket
        self.add_item(close_button)

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

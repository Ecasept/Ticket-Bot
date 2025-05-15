import discord

from header import HeaderView
from utils import C, R, get_support_category, get_support_role, logger
from database import db


class PanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label=R.create_ticket_button, style=discord.ButtonStyle.primary, emoji=discord.PartialEmoji(name=R.create_ticket_emoji), custom_id="create_ticket")
    async def callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(R.choose_category, view=TicketCategorySelection(), ephemeral=True)
        logger.info(
            f"Panel button clicked by {interaction.user.name} (ID: {interaction.user.id})")


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

        channel = await create_new_ticket(interaction.guild, interaction.user, category)

        msg = R.ticket_channel_created % channel.mention
        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            content=msg, view=None)


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
    view = HeaderView()
    msg = R.header_msg_application if category == C.cat_application else R.header_msg_report
    await channel.send(
        content=msg % user.mention,
        view=view
    )

    logger.info(
        f"Ticket channel initialized for {user.name} (ID: {user.id})")


async def create_new_ticket(guild: discord.Guild, user: discord.User, category: str):
    channel = await create_ticket_channel(guild, user, category)
    db.create_ticket(
        str(channel.id),
        category,
        str(user.id),
        None
    )
    await init_ticket_channel(guild, user, channel, category)
    return channel

"""
Implements the PanelView and ticket creation logic for the Discord bot, including UI for ticket category selection and channel creation.
"""
import discord

from src.header import HeaderView
from src.utils import C, R, error_embed, get_ticket_category, get_support_role, logger, create_embed
from src.database import db


class PanelView(discord.ui.View):
    """
    A Discord UI view for the main ticket panel, allowing users to create new tickets.
    """

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label=R.create_ticket_button, style=discord.ButtonStyle.primary, emoji=discord.PartialEmoji(name=R.create_ticket_emoji), custom_id="create_ticket")
    async def callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        Handles the creation of a new ticket when the panel button is clicked.
        """
        await interaction.response.send_message(embed=create_embed(R.choose_category, title=R.ticket_category_title), view=TicketCategorySelection(), ephemeral=True)
        logger.info("panel",
                    f"Panel button clicked by {interaction.user.name} (ID: {interaction.user.id})")


class TicketCategorySelection(discord.ui.View):
    """
    A Discord UI view for selecting the ticket category (application, report, or support).
    """
    @discord.ui.select(
        placeholder=R.ticket_category_placeholder,
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label=R.application, value=C.cat_application, description=R.application_desc),
            discord.SelectOption(
                label=R.report, value=C.cat_report, description=R.report_desc),
            discord.SelectOption(
                label=R.support, value=C.cat_support, description=R.support_desc),
        ],
    )
    async def callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        """
        Handles the selection of a ticket category and initiates ticket creation.
        """
        category = select.values[0]

        info = None
        if category == C.cat_application:
            # Let the user input Information for the application
            info = await self.get_application_info(interaction)
            if info is None:
                # User cancelled the modal
                return
        else:
            await interaction.response.defer(ephemeral=True)

        channel = await create_new_ticket(interaction, interaction.user, category, info)

        msg = R.ticket_channel_created % channel.mention
        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            embed=create_embed(msg, color=C.success_color), view=None)

    async def get_application_info(self, interaction: discord.Interaction) -> dict | None:
        """
        Show a modal to the user to get their application information.
        Args:
            interaction (discord.Interaction): The Discord interaction.
        Returns:
            dict: A dictionary containing the user's application information.
            None: If the user cancels the modal.
        """
        modal = ApplicationModal()
        logger.info(
            "panel", f"Application modal opened for {interaction.user.name} (ID: {interaction.user.id})"
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        if modal.age is None or modal.apply_for is None or modal.application_text is None:
            # User cancelled or closed the modal
            # Doesn't work currently as modal.wait() just won't ever return
            # if the modal is cancelled
            await interaction.respond(
                embed=create_embed(R.application_cancelled,
                                   color=C.warning_color),
                ephemeral=True
            )
            return None
        return {
            "age": modal.age.value,
            "apply_for": modal.apply_for.value,
            "application_text": modal.application_text.value
        }


class ApplicationModal(discord.ui.Modal):
    """
    A modal for collecting additional information from the user when creating an application ticket.
    """

    def __init__(self):
        super().__init__(title=R.application)
        self.age = discord.ui.InputText(
            label=R.application_age_label, placeholder=R.application_age_placeholder, required=True, style=discord.InputTextStyle.short)
        self.apply_for = discord.ui.InputText(label=R.application_apply_for_label,
                                              placeholder=R.application_apply_for_placeholder, required=True, style=discord.InputTextStyle.short)
        self.application_text = discord.ui.InputText(
            label=R.application_text_label, placeholder=R.application_text_placeholder, required=True, style=discord.InputTextStyle.long)
        self.add_item(self.age)
        self.add_item(self.apply_for)
        self.add_item(self.application_text)

    async def callback(self, interaction: discord.Interaction):
        # Acknowledge the interaction
        await interaction.response.defer(ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        logger.error("panel", f"Error in ApplicationModal: {error}")
        await interaction.respond(
            embed=error_embed(R.error_occurred), ephemeral=True)


def generate_channel_name(user: discord.User, category: str):
    """
    Generate a unique channel name for a ticket based on the user and category.
    Args:
        user (discord.User): The user creating the ticket.
        category (str): The ticket category.
    Returns:
        str: The generated channel name.
    """
    match category:
        case C.cat_application:
            prefix = R.application_prefix
        case C.cat_report:
            prefix = R.report_prefix
        case C.cat_support:
            prefix = R.support_prefix
        case _:
            logger.error(
                "panel", f"Invalid category {category} for channel name generation.")
            prefix = R.support_prefix

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


async def create_ticket_channel(interaction: discord.Interaction, user: discord.User, category: str):
    """
    Create a new text channel for the ticket in the support category.
    Args:
        interaction (discord.Interaction): The Discord interaction.
        user (discord.User): The user creating the ticket.
        category (str): The ticket category.
    Returns:
        discord.TextChannel: The created channel.
    """
    ticket_category = await get_ticket_category(interaction)

    channel_name = generate_channel_name(user, category)
    support_role = get_support_role(interaction.guild)

    channel = await interaction.guild.create_text_channel(
        name=channel_name,
        category=ticket_category,
        overwrites={
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
            support_role: discord.PermissionOverwrite(read_messages=True),
            user: discord.PermissionOverwrite(read_messages=True)
        }
    )

    logger.info(
        "panel", f"Ticket channel created for {user.name} (ID: {user.id})")
    return channel


async def init_ticket_channel(interaction: discord.Interaction, user: discord.User, channel: discord.TextChannel, category: str, info: dict | None = None):
    """
    Initialize the ticket channel with a header message and view.
    Args:
        interaction (discord.Interaction): The Discord interaction.
        user (discord.User): The user who created the ticket.
        channel (discord.TextChannel): The ticket channel.
        category (str): The ticket category.
        info (dict | None): Additional information for the ticket (e.g., application details).
    """
    view = HeaderView()
    match category:
        case C.cat_application:
            msg = R.header_msg_application
            title = R.header_title_application
        case C.cat_report:
            msg = R.header_msg_report
            title = R.header_title_report
        case C.cat_support:
            msg = R.header_msg_support
            title = R.header_title_support
        case _:
            logger.error(
                "panel", f"Invalid category {category} for ticket channel initialization.")
            msg = R.header_msg_support
            title = R.header_title_support
    embed = discord.Embed(
        title=title,
        description=msg % user.mention,
        color=C.embed_color,
    )

    if category == C.cat_application and info is not None:
        embed.add_field(name=R.application_age_label,
                        value=info.get("age"), inline=False)
        embed.add_field(name=R.application_apply_for_label,
                        value=info.get("apply_for"), inline=False)
        embed.add_field(name=R.application_text_label,
                        value=info.get("application_text"), inline=False)

    embed.set_footer(text=R.header_footer % str(channel.id))
    embed.set_author(
        name=user.name,
        icon_url=user.display_avatar.url
    )

    await channel.send(
        content=user.mention,
        embed=embed,
        view=view
    )

    logger.info("panel",
                f"Ticket channel initialized for {user.name} (ID: {user.id})")


async def create_new_ticket(interaction: discord.Interaction, user: discord.User, category: str, info: dict | None = None):
    """
    Create a new ticket: channel, database entry, and header message.
    Args:
        interaction (discord.Interaction): The Discord interaction.
        user (discord.User): The user creating the ticket.
        category (str): The ticket category.
        info (dict | None): Additional information for the ticket (e.g., application details).
    Returns:
        discord.TextChannel: The created ticket channel.
    """
    channel = await create_ticket_channel(interaction, user, category)
    db.create_ticket(
        str(channel.id),
        category,
        str(user.id),
        None
    )
    await init_ticket_channel(interaction, user, channel, category, info)
    return channel

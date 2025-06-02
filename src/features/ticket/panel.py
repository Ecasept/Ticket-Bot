"""
Implements the PanelView and ticket creation logic for the Discord bot, including UI for ticket category selection and channel creation.
"""
import discord

from .header import HeaderView
from src.utils import get_mod_roles, get_ticket_category, logger, create_embed, handle_error
from src.database import db
from src.res import C, R
from src.error import Ce


class PanelView(discord.ui.View):
    """
    A Discord UI view for the main ticket panel, allowing users to create new tickets by selecting a category directly.
    """

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label=R.application, style=discord.ButtonStyle.secondary, emoji=discord.PartialEmoji(name=R.application_emoji), custom_id="create_application_ticket")
    async def application_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        info = await self.get_application_info(interaction)
        if info is None:
            return
        channel = await create_new_ticket(interaction, interaction.user, C.cat_application, info)
        if channel is None:
            return
        msg = R.ticket_channel_created % channel.mention
        await interaction.followup.send(
            embed=create_embed(msg, color=C.success_color), ephemeral=True)

    @discord.ui.button(label=R.report, style=discord.ButtonStyle.secondary, emoji=discord.PartialEmoji(name=R.report_emoji), custom_id="create_report_ticket")
    async def report_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        channel = await create_new_ticket(interaction, interaction.user, C.cat_report)
        if channel is None:
            return
        msg = R.ticket_channel_created % channel.mention
        await interaction.followup.send(
            embed=create_embed(msg, color=C.success_color), ephemeral=True)

    @discord.ui.button(label=R.support, style=discord.ButtonStyle.secondary, emoji=discord.PartialEmoji(name=R.support_emoji), custom_id="create_support_ticket")
    async def support_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        channel = await create_new_ticket(interaction, interaction.user, C.cat_support)
        if channel is None:
            return
        msg = R.ticket_channel_created % channel.mention
        await interaction.followup.send(
            embed=create_embed(msg, color=C.success_color), ephemeral=True)

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
        await interaction.response.send_modal(modal)
        logger.info("Application modal opened", interaction)
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
        # The modal data will be accessed later via the modal instance properties

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        """
        Handle errors that occur in the ApplicationModal.
        Args:
            interaction (discord.Interaction): The interaction that caused the error.
            error (Exception): The exception that occurred.
        """
        err = Ce(f"Error in ApplicationModal: {error}")
        logger.error(err, interaction)
        await handle_error(interaction, err)


def generate_channel_name(user: discord.User, category: str) -> str:
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
            err = Ce(
                f"Invalid category {category} for channel name generation.")
            logger.error(err)
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


async def create_ticket_channel(interaction: discord.Interaction, user: discord.User, category: str) -> discord.TextChannel | None:
    """
    Create a new text channel for the ticket in the support category.
    Args:
        interaction (discord.Interaction): The Discord interaction.
        user (discord.User): The user creating the ticket.
        category (str): The ticket category.
    Returns:
        discord.TextChannel: The created ticket channel.
        None: If the ticket category is not found or an error occurs.
    """
    ticket_category, err = await get_ticket_category(interaction.guild)
    if err:
        await handle_error(interaction, err)
        return None

    channel_name = generate_channel_name(user, category)

    mod_roles, err = get_mod_roles(interaction.guild)
    if err:
        await handle_error(interaction, err)
        return None

    overwrites = {
        user: discord.PermissionOverwrite(read_messages=True),
        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
    }
    for role in mod_roles:
        # Allow moderators to read the ticket channel
        overwrites[role] = discord.PermissionOverwrite(read_messages=True)

    channel = await interaction.guild.create_text_channel(
        name=channel_name,
        category=ticket_category,
        overwrites=overwrites,
    )

    logger.info(
        f"Ticket channel #{channel.name} (ID: {channel.id}) created", interaction)
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
            logger.error(Ce(f"Invalid category {category} for ticket channel initialization, "
                            f"using support as default."), interaction)
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

    logger.info(
        f"Ticket channel #{channel.name} (ID: {channel.id}) initialized", interaction)


async def create_new_ticket(interaction: discord.Interaction, user: discord.User, category: str, info: dict | None = None) -> discord.TextChannel | None:
    """
    Create a new ticket: channel, database entry, and header message.
    Args:
        interaction (discord.Interaction): The Discord interaction.
        user (discord.User): The user creating the ticket.
        category (str): The ticket category.
        info (dict | None): Additional information for the ticket (e.g., application details).
    Returns:
        discord.TextChannel: The created ticket channel.
        None: If an error occurs during ticket creation.
    """
    channel = await create_ticket_channel(interaction, user, category)
    if channel is None:
        # Error ocurred
        return None
    db.create_ticket(
        str(channel.id),
        category,
        str(user.id),
        None
    )
    await init_ticket_channel(interaction, user, channel, category, info)
    return channel

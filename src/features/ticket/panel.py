"""
Implements the PanelView and ticket creation logic for the Discord bot, including UI for ticket category selection and channel creation.
"""
import discord

from src.database.ticket_category import TicketCategory

from .header import HeaderView
from src.utils import get_mod_roles, get_ticket_category, logger, create_embed, handle_error
from src.database import db
from src.constants import C
from src.res import R
from src.error import Ce, We
from src.features.category.questions import CategoryQuestionsModal


class PanelView(discord.ui.View):
    """
    A Discord UI view for the main ticket panel, allowing users to create new tickets by selecting a category directly.
    """

    def __init__(self):
        super().__init__(timeout=None)

    async def init(self, interaction: discord.Interaction | None = None):
        categories = []
        err = None
        if interaction is None:
            # This is the initialization for the persistent view
            # Just add a mock category
            categories = [
                TicketCategory(
                    id=0,
                    name=R.feature.panel.test_category_name,
                    emoji="🎫",
                    description=R.feature.panel.test_category_description,
                    guild_id=0
                )
            ]
        else:
            categories = db.tc.get_categories_for_guild(interaction.guild.id)

        if not categories:
            # No categories available - user has no access or none configured
            return False

        # Create dropdown menu for categories
        dropdown = await self._create_category_dropdown(categories, interaction)
        if dropdown:
            self.add_item(dropdown)
        else:
            # No categories to show
            await handle_error(interaction, We(R.feature.panel.no_categories_found))

    async def _create_category_dropdown(self, categories, interaction: discord.Interaction):
        """Create a dropdown menu for category selection."""
        options = []

        for category in categories[:25]:  # Discord limit for select options

            emoji = category.emoji.strip()
            if emoji.startswith(":") and emoji.endswith(":"):
                emoji = discord.utils.get(
                    interaction.guild.emojis, name=emoji[1:-1])
            else:
                emoji = discord.PartialEmoji.from_str(emoji)

            options.append(discord.SelectOption(
                label=category.name,
                value=str(category.id),
                description=category.description[:100] if category.description else R.feature.panel.no_description,
                emoji=emoji
            ))

        if not options:
            return None

        select = discord.ui.Select(
            placeholder=R.ticket_category_select_placeholder,
            options=options,
            custom_id="category_select"
        )

        async def callback(select_interaction: discord.Interaction):
            category_id = int(select_interaction.data["values"][0])
            await self.handle_category_selection(select_interaction, category_id)

        select.callback = callback
        return select

    async def handle_category_selection(self, interaction: discord.Interaction, category_id: int):
        """Handle ticket creation for a selected category."""
        try:
            # Get category details
            category = db.tc.get_category(category_id)
            if not category:
                await handle_error(interaction, We(R.feature.panel.category_not_found))
                return

            # Check if user can use this category
            user_role_ids = [role.id for role in interaction.user.roles]
            if not db.tc.user_can_use_category(category_id, user_role_ids):
                await handle_error(interaction, We(R.feature.panel.no_permission))
                return

            # Check for questions
            questions = db.tc.get_questions(category_id)

            if questions:
                # Show modal with questions
                modal = CategoryQuestionsModal(category, questions)
                await interaction.response.send_modal(modal)
                await modal.wait()

                if modal.answers is None:
                    return  # User cancelled

                # Create ticket with answers
                formatted_answers = modal.get_formatted_answers()
                channel = await create_new_ticket(interaction, interaction.user, category_id, question_answers=formatted_answers)
            else:
                # Create ticket directly
                await interaction.response.defer(ephemeral=True)
                channel = await create_new_ticket(interaction, interaction.user, category_id)

            if channel is None:
                return

            msg = R.ticket_channel_created % channel.mention
            if interaction.response.is_done():
                await interaction.followup.send(
                    embed=create_embed(msg, color=C.success_color), ephemeral=True)
            else:
                await interaction.response.send_message(
                    embed=create_embed(msg, color=C.success_color), ephemeral=True)

        except Exception as e:
            logger.error(f"Error handling category selection: {e}")
            await handle_error(interaction, Ce(R.feature.panel.error_creating_ticket % e))


def generate_channel_name(user: discord.User, category_name: str) -> str:
    """
    Generate a unique channel name for a ticket based on the user and category.
    Args:
        user (discord.User): The user creating the ticket.
        category_name (str): The ticket category name.
    Returns:
        str: The generated channel name.
    """
    # Convert category name to a safe prefix
    replacements = {
        " ": "-", "ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"
    }
    prefix = category_name.lower()
    for old, new in replacements.items():
        prefix = prefix.replace(old, new)

    # Remove any non-alphanumeric characters except hyphens
    import re
    prefix = re.sub(r'[^a-z0-9\-]', '', prefix)

    # Fallback prefixes for known categories
    if not prefix:
        prefix = R.feature.panel.default_category_name

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


async def create_ticket_channel(interaction: discord.Interaction, user: discord.User, category_id: int) -> discord.TextChannel | None:
    """
    Create a new text channel for the ticket in the support category.
    Args:
        interaction (discord.Interaction): The Discord interaction.
        user (discord.User): The user creating the ticket.
        category_id (int): The ticket category ID.
    Returns:
        discord.TextChannel: The created ticket channel.
        None: If the ticket category is not found or an error occurs.
    """
    ticket_category, err = await get_ticket_category(interaction.guild)
    if err:
        await handle_error(interaction, err)
        return None

    # Get category name for channel naming
    category = db.tc.get_category(category_id)
    category_name = category.name if category else R.feature.panel.default_category_name

    channel_name = generate_channel_name(user, category_name)

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


async def init_ticket_channel(interaction: discord.Interaction, user: discord.User, channel: discord.TextChannel, category_id: int, question_answers: str | None = None):
    """
    Initialize the ticket channel with a header message and view.
    Args:
        interaction (discord.Interaction): The Discord interaction.
        user (discord.User): The user who created the ticket.
        channel (discord.TextChannel): The ticket channel.
        category_id (int): The ticket category ID.
        question_answers (str | None): Formatted answers to category questions.
    """
    view = HeaderView()

    # Get category details
    category = db.tc.get_category(category_id)
    title = f"{category.emoji} {category.name}"
    msg = R.feature.panel.welcome_message % (user.mention, category.description)

    embed = discord.Embed(
        title=title,
        description=msg,
        color=C.embed_color,
    )

    # Add category question answers if present
    if question_answers:
        embed.add_field(
            name=R.feature.panel.answers,
            value=question_answers,
            inline=False
        )

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


async def create_new_ticket(interaction: discord.Interaction, user: discord.User, category_id: int, question_answers: str | None = None) -> discord.TextChannel | None:
    """
    Create a new ticket: channel, database entry, and header message.
    Args:
        interaction (discord.Interaction): The Discord interaction.
        user (discord.User): The user creating the ticket.
        category_id (int): The ticket category ID.
        question_answers (str | None): Formatted answers to category questions.
    Returns:
        discord.TextChannel: The created ticket channel.
        None: If an error occurs during ticket creation.
    """
    channel = await create_ticket_channel(interaction, user, category_id)
    if channel is None:
        # Error occurred
        return None
    db.ticket.create(
        str(channel.id),
        category_id,
        str(user.id),
        None
    )
    await init_ticket_channel(interaction, user, channel, category_id, question_answers)
    return channel


async def create_panel_view(guild_id: int, interaction: discord.Interaction | None) -> tuple[PanelView, We | Ce | None]:
    """
    Create a panel view with dynamic category dropdown selection.
    Only shows categories that the user has permission to access.

    Args:
        guild_id (int): The Discord guild ID.

    Returns:
        tuple: (PanelView, Error) - The panel view and any error that occurred.
    """
    try:
        # Check if guild has any categories
        categories = db.tc.get_categories_for_guild(guild_id)

        if not categories:
            return None, We(R.feature.panel.no_categories_configured_error)

        # Create the persistent panel view with dynamic dropdown menu
        panel_view = PanelView()
        await panel_view.init(interaction)

        return panel_view, None

    except Exception as e:
        logger.error(f"Error creating panel view: {e}")
        return None, Ce(R.feature.panel.panel_view_error % e)

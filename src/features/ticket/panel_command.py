"""
Panel command for creating ticket panels.
"""
import discord
from src.res import R, RD, RL
from src.constants import C
from src.utils import create_embed, handle_error, is_valid_url, logger
from src.error import We, Ce
from src.features.ticket.panel import create_panel_view

from src.custom_bot import CustomBot


def setup_panel_command(bot: CustomBot):
    """
    Setup the panel command for the bot.
    Args:
        bot (CustomBot): The Discord bot instance.
    """

    @bot.slash_command(
        name=RD.command.createpanel.name,
        name_localizations=RL.command.createpanel.name,
        description=RD.command.createpanel.desc,
        description_localizations=RL.command.createpanel.desc
    )
    @discord.default_permissions(administrator=True)
    @discord.option(
        parameter_name="image_url",
        name=RD.command.createpanel.option.image_url,
        name_localizations=RL.command.createpanel.option.image_url,
        description=RD.command.createpanel.option.image_url_desc,
        description_localizations=RL.command.createpanel.option.image_url_desc,
        type=discord.SlashCommandOptionType.string,
        required=False,
        default=None
    )
    async def create_panel(ctx: discord.ApplicationContext, image_url: str | None = None):
        """
        Create a new ticket panel in the current channel.
        Args:
            ctx (discord.ApplicationContext): The command context.
        """
        if image_url:
            image_url = image_url.strip()
            if not is_valid_url(image_url):
                await handle_error(ctx.interaction, We(R.feature.panel.invalid_image_url))
                return

        # Create panel view with error handling
        panel_view, err = await create_panel_view(ctx.guild.id, ctx.interaction)

        if err:
            await handle_error(ctx.interaction, err)
            return

        panel_embed = create_embed(
            None if image_url else R.panel_msg, title=R.ticket_panel_title)
        if image_url:
            panel_embed.set_image(url=image_url)

        await ctx.send(embed=panel_embed, view=panel_view)
        await ctx.respond(embed=create_embed(R.ticket_msg_created, color=C.success_color, title=R.ticket_panel_title), ephemeral=True)
        logger.info("Panel created", ctx.interaction)

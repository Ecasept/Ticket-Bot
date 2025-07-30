"""
Panel command for creating ticket panels.
"""
import discord
from src.res import R, RD, RL
from src.constants import C
from src.utils import create_embed, handle_error, logger
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
    async def create_panel(ctx: discord.ApplicationContext):
        """
        Create a new ticket panel in the current channel.
        Args:
            ctx (discord.ApplicationContext): The command context.
        """
        # Create panel view with error handling
        panel_view, err = await create_panel_view(ctx.guild.id, ctx.interaction)

        if err:
            await handle_error(ctx.interaction, err)
            return

        await ctx.send(embed=create_embed(R.panel_msg, title=R.ticket_panel_title), view=panel_view)
        await ctx.respond(embed=create_embed(R.ticket_msg_created, color=C.success_color, title=R.ticket_panel_title), ephemeral=True)
        logger.info("Panel created", ctx.interaction)

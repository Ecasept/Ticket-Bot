"""
Main entry point for the Discord bot. Handles bot events, command registration, and startup/shutdown logic.
"""
import discord

from .features.ticket_menu.ticket_menu import TicketMenuView
from .features.ticket.noch_fragen import NochFragenMessage, setup_noch_fragen
from .features.ticket.close_request import TicketCloseRequestView
from .features.ticket.closed import ClosedView
from .features.ticket.panel import PanelView
from .features.ticket.panel_command import setup_panel_command
from .features.ticket.header import HeaderView
from .utils import MODE, TOKEN, logger, create_embed
from .error import We, Ce
from .database import db
from .features.team import TeamListMessage, setup_team_command
from .features.banlist.command import setup_banlist_command, update_banlist
from .features.shared.list_display import ListDisplayView
from .help import setup_help_command
from .res import C, R
from .features.ticket_menu.ticket_command import setup_ticket_command
from .features.giveaway.command import setup_giveaway_command
from .features.timeout.command import setup_timeout_command
from .features.setup.command import setup_setup_command
from .features.category.command import setup_category_command
from .features.lang.command import setup_lang_command
import traceback

intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    logger.info(f"Connected to {len(bot.guilds)} guilds:")
    logger.info(f"Starting in mode: {MODE}")
    for guild in bot.guilds:
        logger.info(f" - {guild.name} (ID: {guild.id})")
    logger.info("------")

    activity = discord.Game(name=R.bot_activity)
    await bot.change_presence(activity=activity)

    # Register views as persistent
    # This is required to make them work after a restart
    pv = PanelView()
    await pv.init(None)
    bot.add_view(pv)
    bot.add_view(HeaderView())
    bot.add_view(TicketCloseRequestView())
    bot.add_view(ClosedView())
    bot.add_view(ListDisplayView(
        "update_team_list", TeamListMessage.update_team_list))
    bot.add_view(ListDisplayView(
        "update_banlist", update_banlist))
    bot.add_view(NochFragenMessage())
    bot.add_view(TicketMenuView())


@bot.slash_command(name="ping", description=R.ping_desc)
async def ping(ctx: discord.ApplicationContext):
    """
    Simple ping command to test bot responsiveness.
    Args:
        ctx (discord.ApplicationContext): The command context.
    """
    await ctx.respond("Pong!")
    logger.info("Ping command executed", ctx.interaction)

setup_panel_command(bot)
setup_setup_command(bot)
setup_noch_fragen(bot)
setup_giveaway_command(bot)
setup_timeout_command(bot)
setup_ticket_command(bot)
setup_category_command(bot)
setup_lang_command(bot)
setup_team_command(bot)
setup_banlist_command(bot)
setup_help_command(bot)

try:
    if TOKEN is None:
        raise ValueError(
            "DISCORD_TOKEN is not set in the environment variables.")
    logger.info("Starting bot...")

    db.connect()
    bot.run(TOKEN)
except KeyboardInterrupt:
    logger.info("Bot has been stopped by user.")
except Exception as e:
    logger.error(Ce(f"Failed to run the bot: {traceback.format_exc()}"))
finally:
    db.close()
    logger.info("Bot has been shut down.")
    logger.info("------")

"""
Main entry point for the Discord bot. Handles bot events, command registration, and startup/shutdown logic.
"""
import discord

from .features.timeout import setup_timeout_commands
from .features.ticket.noch_fragen import NochFragenMessage, setup_noch_fragen
from .features.setup import setup_setup_command
from .features.ticket.close_request import TicketCloseRequestView
from .features.ticket.closed import ClosedView
from .features.ticket.panel import PanelView
from .features.ticket.header import HeaderView
from .features.giveaway import setup_giveaway_command
from .utils import TOKEN, logger, create_embed
from .error import We
from .database import db
from .features.team import setup_team_command, TeamListMessage
from .help import setup_help_command
from .res import C, R
import traceback

intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    logger.info(f"Connected to {len(bot.guilds)} guilds:")
    for guild in bot.guilds:
        logger.info(f" - {guild.name} (ID: {guild.id})")
    logger.info("------")

    activity = discord.Game(name=R.bot_activity)
    await bot.change_presence(activity=activity)

    # Register views as persistent
    # This is required to make them work after a restart
    bot.add_view(PanelView())
    bot.add_view(HeaderView())
    bot.add_view(TicketCloseRequestView())
    bot.add_view(ClosedView())
    bot.add_view(TeamListMessage())
    bot.add_view(NochFragenMessage())


@bot.slash_command(name="createpanel", description=R.ticket_msg_desc)
@discord.default_permissions(administrator=True)
async def create_panel(ctx: discord.ApplicationContext):
    """
    Create a new ticket panel in the current channel.
    Args:
        ctx (discord.ApplicationContext): The command context.
    """
    await ctx.send(embed=create_embed(R.panel_msg, title=R.ticket_panel_title), view=PanelView())
    await ctx.respond(embed=create_embed(R.ticket_msg_created, color=C.success_color, title=R.ticket_panel_title), ephemeral=True)
    logger.info("Panel created", ctx.interaction)


@bot.slash_command(name="ping", description=R.ping_desc)
async def ping(ctx: discord.ApplicationContext):
    """
    Simple ping command to test bot responsiveness.
    Args:
        ctx (discord.ApplicationContext): The command context.
    """
    await ctx.respond("Pong!")
    logger.info("Ping command executed", ctx.interaction)

setup_setup_command(bot)
setup_team_command(bot)
setup_help_command(bot)
setup_noch_fragen(bot)
setup_giveaway_command(bot)
setup_timeout_commands(bot)


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
    logger.error(We(f"Failed to run the bot: {traceback.format_exc()}"))
finally:
    db.close()
    logger.info("Bot has been shut down.")
    logger.info("------")

"""
Main entry point for the Discord bot. Handles bot events, command registration, and startup/shutdown logic.
"""
import discord
from src.noch_fragen import NochFragenMessage, setup_noch_fragen
from src.setup import setup_setup_command
from src.close_request import TicketCloseRequestView
from src.closed import ClosedView
from src.panel import PanelView
from src.header import HeaderView
from src.utils import R, C, TOKEN, logger, create_embed
from src.database import db
from src.team_list import setup_team_list_command, TeamListMessage
from src.help import setup_help_command

intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    logger.info("event", f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    logger.info("event", "------")
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
    await ctx.send(embed=create_embed(R.panel_msg, title=R.ticket_panel_title), view=PanelView())
    await ctx.respond(embed=create_embed(R.ticket_msg_created, color=C.success_color, title=R.ticket_panel_title), ephemeral=True)
    logger.info("cmd", f"Panel created by {ctx.user.name} (ID: {ctx.user.id})")


@bot.slash_command(name="ping", description=R.ping_desc)
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond("Pong!")
    logger.info(
        "cmd", f"Ping command used by {ctx.user.name} (ID: {ctx.user.id})")

setup_setup_command(bot)
setup_team_list_command(bot)
setup_help_command(bot)
setup_noch_fragen(bot)


try:
    if TOKEN is None:
        raise ValueError(
            "DISCORD_TOKEN is not set in the environment variables.")
    logger.info("main", "Starting bot...")

    db.connect()
    bot.run(TOKEN)
except KeyboardInterrupt:
    logger.info("main", "Bot has been stopped by user.")
except Exception as e:
    logger.error("main", f"Failed to run the bot: {e}")
finally:
    db.close()
    logger.info("main", "Bot has been shut down.")
    logger.info("main", "------")

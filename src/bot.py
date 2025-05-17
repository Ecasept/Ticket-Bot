"""
Main entry point for the Discord bot. Handles bot events, command registration, and startup/shutdown logic.
"""
import discord
from src.close_request import TicketCloseRequestView
from src.closed import ClosedView
from src.panel import PanelView
from src.header import HeaderView
from src.utils import R, TOKEN, logger
from src.database import db

bot = discord.Bot()


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


@bot.slash_command(name="createpanel", description=R.ticket_msg_desc)
@discord.default_permissions(administrator=True)
async def create_panel(ctx: discord.ApplicationContext):
    await ctx.send(R.panel_msg, view=PanelView())
    await ctx.respond(R.ticket_msg_created, ephemeral=True)
    logger.info("cmd", f"Panel created by {ctx.user.name} (ID: {ctx.user.id})")


@bot.slash_command(name="ping", description=R.ping_desc)
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond("Pong!")
    logger.info(
        "cmd", f"Ping command used by {ctx.user.name} (ID: {ctx.user.id})")

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

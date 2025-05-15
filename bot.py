import discord
from panel import PanelView
from header import HeaderView
from utils import R, TOKEN, logger
from database import db

bot = discord.Bot()


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    logger.info("------")
    # Register views as persistent
    # This is required to make them work after a restart
    bot.add_view(PanelView())
    bot.add_view(HeaderView())


@bot.slash_command(name="createpanel", description=R.ticket_msg_desc)
@discord.default_permissions(administrator=True)
async def create_panel(ctx: discord.ApplicationContext):
    await ctx.send(R.panel_msg, view=PanelView())
    await ctx.respond(R.ticket_msg_created, ephemeral=True)
    logger.info(f"Panel created by {ctx.user.name} (ID: {ctx.user.id})")


@bot.slash_command(name="ping", description=R.ping_desc)
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond("Pong!")
    logger.info(f"Ping command used by {ctx.user.name} (ID: {ctx.user.id})")

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
    logger.error(f"Failed to run the bot: {e}")
finally:
    db.close()
    logger.info("Bot has been shut down.")
    logger.info("------")

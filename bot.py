import discord
from category_selection import TicketCategorySelection
from ticket import TicketOptionsMessage
from utils import C, R, TOKEN, get_support_role, logger
import dynamic
import database

bot = discord.Bot()
db = database.Database(C.db_file)


class PanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label=R.create_ticket_button, style=discord.ButtonStyle.primary, emoji=discord.PartialEmoji(name=R.create_ticket_emoji), custom_id="create_ticket")
    async def callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(R.choose_category, view=TicketCategorySelection(), ephemeral=True)
        logger.info(
            f"Panel button clicked by {interaction.user.name} (ID: {interaction.user.id})")


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    logger.info("------")
    # Register views as persistent
    # This is required to make them work after a restart
    bot.add_view(PanelView())
    dynamic.add_dynamic_view(TicketOptionsMessage)


@bot.slash_command(name="createpanel", description=R.ticket_msg_desc)
@discord.default_permissions(administrator=True)
async def create_panel(ctx: discord.ApplicationContext):
    await ctx.send(R.panel_msg, view=PanelView())
    await ctx.respond(R.ticket_msg_created, ephemeral=True)
    logger.info(f"Panel created by {ctx.user.name} (ID: {ctx.user.id})")


@bot.event
async def on_interaction(interaction: discord.Interaction):
    await dynamic.resolve_interaction(interaction)


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

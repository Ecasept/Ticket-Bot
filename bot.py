# Installation: pip install discord.py dotenv

import discord
import log
import dotenv
import os
import res

dotenv.load_dotenv()

logger = log.Logger("bot.log")
TOKEN = os.getenv("DISCORD_TOKEN")

R = res.get_resources("de")
C = res.Constants()

bot = discord.Bot()


class TicketCreaterView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label=R.create_ticket_button, style=discord.ButtonStyle.primary, emoji=discord.PartialEmoji(name=R.create_ticket_emoji), custom_id="create_ticket")
    async def callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        channel = await create_ticket_channel(interaction.guild, interaction.user)
        await init_ticket_channel(interaction.guild, interaction.user, channel)

        msg = R.ticket_channel_created % channel.mention
        await interaction.response.send_message(msg, ephemeral=True)


async def init_ticket_channel(guild: discord.Guild, user: discord.User, channel: discord.TextChannel):
    await channel.send(
        f"Hallo {user.mention}, willkommen in deinem Ticket-Kanal!"
    )
    logger.info(
        f"Ticket channel initialized for {user.name} (ID: {user.id})")


async def create_ticket_channel(guild: discord.Guild, user: discord.User):
    category = discord.utils.get(
        guild.categories, name=C.support_category_name)
    if category is None:
        category = await guild.create_category(C.support_category_name)

    channel_name = f"{R.ticket}-{user.name}"
    i = 0
    while True:
        channel = discord.utils.get(guild.text_channels, name=channel_name)
        if channel is None:
            break
        i += 1
        channel_name = f"ticket-{user.name}-{i}"

    support_role = discord.utils.get(guild.roles, name=C.support_role_name)

    channel = await guild.create_text_channel(
        name=channel_name,
        category=category,
        overwrites={
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            support_role: discord.PermissionOverwrite(read_messages=True),
            user: discord.PermissionOverwrite(read_messages=True)
        }
    )

    logger.info(f"Ticket channel created for {user.name} (ID: {user.id})")
    return channel


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    logger.info("------")
    # Register view as persistent
    # This is required to make the button work after a restart
    bot.add_view(TicketCreaterView())


@bot.slash_command(name="ticketmessage", description=R.ticket_msg_desc)
@discord.default_permissions(administrator=True)
async def ticket_message(ctx: discord.ApplicationContext):
    await ctx.send(R.create_ticket_msg, view=TicketCreaterView())
    await ctx.respond(R.ticket_msg_created, ephemeral=True)
    logger.info(f"Ticket message sent by {ctx.user.name} (ID: {ctx.user.id})")


@bot.slash_command(name="ping", description=R.ping_desc)
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond("Pong!")
    logger.info(f"Ping command used by {ctx.user.name} (ID: {ctx.user.id})")

try:
    if TOKEN is None:
        raise ValueError(
            "DISCORD_TOKEN is not set in the environment variables.")
    logger.info("Starting bot...")
    bot.run(TOKEN)
except KeyboardInterrupt:
    logger.info("Bot has been stopped by user.")
except Exception as e:
    logger.error(f"Failed to run the bot: {e}")
finally:
    logger.info("Bot has been shut down.")
    logger.info("------")

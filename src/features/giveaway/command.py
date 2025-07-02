"""
Giveaway slash command - separated from functionality.
"""
import discord
from src.res import R
from src.features.giveaway.giveaway import create_giveaway, setup_giveaway_background_task


def setup_giveaway_command(bot: discord.Bot):
    """
    Setup the giveaway command for the bot.
    Args:
        bot (discord.Bot): The Discord bot instance.
    """

    @bot.slash_command(name="giveaway", description=R.giveaway_desc)
    @discord.default_permissions(administrator=True)
    @discord.option(
        "dauer",
        description=R.giveaway_duration_desc,
        required=True
    )
    @discord.option(
        "preis",
        description=R.giveaway_prize_desc,
        required=True
    )
    @discord.option(
        "gewinner",
        description=R.giveaway_winners_desc,
        required=False,
        default=1,
        min_value=1,
        max_value=20
    )
    @discord.option(
        "rolle",
        description=R.giveaway_role_desc,
        required=False,
        default=None,
        type=discord.SlashCommandOptionType.role
    )
    async def giveaway_command(
        interaction: discord.Interaction,
        dauer: str,
        preis: str,
        gewinner: int = 1,
        rolle: discord.Role = None
    ):
        """
        Start a giveaway with automatic winner selection.
        Args:
            interaction (discord.Interaction): The interaction context.
            dauer (str): Duration of the giveaway (e.g., "30s", "2m", "1h").
            preis (str): What is being given away.
            gewinner (int): Number of winners to select.
            rolle (discord.Role): Role to award to winners (optional).
        """
        await create_giveaway(interaction, dauer, preis, gewinner, rolle)

    # Setup background task
    setup_giveaway_background_task(bot)

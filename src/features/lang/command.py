"""
Language command to switch bot language per guild.
"""
import discord
from src.utils import get_guild_resources, set_guild_language, get_guild_language, handle_error, create_embed
from src.res import get_resources


def setup_lang_command(bot: discord.Bot):
    """
    Setup the language command for the bot.
    Args:
        bot (discord.Bot): The Discord bot instance.
    """
    
    @bot.slash_command(name="lang", description="Switch the bot language for this server.")
    @discord.default_permissions(administrator=True)
    @discord.option(
        "language",
        description="Choose the language",
        required=False,
        choices=[
            discord.OptionChoice("Deutsch", "de"),
            discord.OptionChoice("English", "en")
        ]
    )
    async def lang_command(ctx: discord.ApplicationContext, language: str = None):
        """
        Command to switch the bot language for the current guild.
        Args:
            ctx (discord.ApplicationContext): The command context.
            language (str): The language code to switch to (optional).
        """
        guild_id = ctx.guild.id
        
        if language is None:
            # Show current language
            current_lang = get_guild_language(guild_id)
            R = get_resources(current_lang)
            
            embed = create_embed(
                title="🌐 Current Language",
                description=R.lang_current,
                color=discord.Color.blue()
            )
        else:
            # Set new language
            set_guild_language(guild_id, language)
            
            # Get resources for the new language to show confirmation
            R = get_resources(language)
            
            embed = create_embed(
                title="🌐 Language Changed",
                description=R.lang_set_success,
                color=discord.Color.green()
            )
        
        await ctx.respond(embed=embed, ephemeral=True)
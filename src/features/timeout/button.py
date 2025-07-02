"""
Timeout button interface for the ticket menu.
"""
import discord
from src.res import R, C
from src.utils import create_embed, logger
from src.features.timeout.timeout import timeout_user


class TimeoutSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.selected_user = None
        self.selected_duration = None
        self.reason = None

    @discord.ui.user_select(
        placeholder="Wähle einen Benutzer zum Timeout",
        min_values=1,
        max_values=1,
    )
    async def user_select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        self.selected_user = select.values[0]
        await interaction.response.defer()

    @discord.ui.select(
        placeholder="Wähle eine Timeout-Dauer",
        options=[
            discord.SelectOption(
                label="30 Sekunden",
                description="Kurzer Timeout",
                value="30s",
                emoji="⏱️"
            ),
            discord.SelectOption(
                label="5 Minuten",
                description="Standard Timeout",
                value="5m",
                emoji="⏰"
            ),
            discord.SelectOption(
                label="1 Stunde",
                description="Längerer Timeout",
                value="1h",
                emoji="🕐"
            ),
            discord.SelectOption(
                label="1 Tag",
                description="Täglicher Timeout",
                value="1d",
                emoji="📅"
            ),
            discord.SelectOption(
                label="1 Woche",
                description="Wöchentlicher Timeout",
                value="1w",
                emoji="📆"
            )
        ]
    )
    async def duration_select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        self.selected_duration = select.values[0]
        await interaction.response.defer()

    @discord.ui.button(
        label="Timeout ausführen",
        style=discord.ButtonStyle.danger,
        emoji="⏰"
    )
    async def execute_timeout_callback(self, button, interaction: discord.Interaction):
        if not self.selected_user:
            await interaction.response.send_message(
                embed=create_embed("❌ Bitte wähle einen Benutzer aus.", color=C.error_color),
                ephemeral=True
            )
            return
        
        if not self.selected_duration:
            await interaction.response.send_message(
                embed=create_embed("❌ Bitte wähle eine Timeout-Dauer aus.", color=C.error_color),
                ephemeral=True
            )
            return
        
        # Convert user to member if needed
        if isinstance(self.selected_user, discord.User):
            member = interaction.guild.get_member(self.selected_user.id)
            if not member:
                await interaction.response.send_message(
                    embed=create_embed("❌ Benutzer ist nicht auf diesem Server.", color=C.error_color),
                    ephemeral=True
                )
                return
        else:
            member = self.selected_user
        
        await timeout_user(interaction, member, self.selected_duration, self.reason)
        self.stop()

    @discord.ui.button(
        label="Abbrechen",
        style=discord.ButtonStyle.secondary,
        emoji="❌"
    )
    async def cancel_callback(self, button, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed=create_embed("Timeout abgebrochen.", color=C.warning_color),
            view=None
        )
        self.stop()


class TimeoutButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label=R.ticket_menu_timeout,
            style=discord.ButtonStyle.secondary,
            emoji="⏰",
            custom_id="ticket_menu_timeout"
        )

    async def callback(self, interaction: discord.Interaction):
        embed = create_embed(
            "Wähle einen Benutzer und eine Timeout-Dauer aus den Dropdown-Menüs:",
            title="Benutzer Timeout",
            color=C.embed_color
        )
        view = TimeoutSelectView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        logger.info("Timeout select menu opened", interaction)

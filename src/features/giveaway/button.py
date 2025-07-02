"""
Giveaway button interface for the ticket menu.
"""
import discord
from src.res import R, C
from src.utils import create_embed, logger
from src.features.giveaway.giveaway import create_giveaway


class GiveawayConfigView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.selected_duration = None
        self.prize = None
        self.winner_count = 1
        self.selected_role = None

    @discord.ui.select(
        placeholder="Wähle eine Giveaway-Dauer",
        options=[
            discord.SelectOption(
                label="30 Sekunden",
                description="Test-Giveaway",
                value="30s",
                emoji="⚡"
            ),
            discord.SelectOption(
                label="5 Minuten",
                description="Kurzes Giveaway",
                value="5m",
                emoji="⏱️"
            ),
            discord.SelectOption(
                label="1 Stunde",
                description="Standard Giveaway",
                value="1h",
                emoji="⏰"
            ),
            discord.SelectOption(
                label="1 Tag",
                description="Tägliches Giveaway",
                value="1d",
                emoji="📅"
            ),
            discord.SelectOption(
                label="1 Woche",
                description="Wöchentliches Giveaway",
                value="1w",
                emoji="📆"
            )
        ]
    )
    async def duration_select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        self.selected_duration = select.values[0]
        await interaction.response.defer()

    @discord.ui.select(
        placeholder="Anzahl Gewinner wählen",
        options=[
            discord.SelectOption(label="1 Gewinner", value="1", emoji="🥇"),
            discord.SelectOption(label="2 Gewinner", value="2", emoji="🥈"),
            discord.SelectOption(label="3 Gewinner", value="3", emoji="🥉"),
            discord.SelectOption(label="5 Gewinner", value="5", emoji="🏆"),
            discord.SelectOption(label="10 Gewinner", value="10", emoji="🎊")
        ]
    )
    async def winner_count_select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        self.winner_count = int(select.values[0])
        await interaction.response.defer()

    @discord.ui.role_select(
        placeholder="Wähle eine Rolle als Preis (optional)",
        min_values=0,
        max_values=1,
    )
    async def role_select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        self.selected_role = select.values[0] if select.values else None
        await interaction.response.defer()

    @discord.ui.button(
        label="Preis eingeben",
        style=discord.ButtonStyle.primary,
        emoji="🎁"
    )
    async def set_prize_callback(self, button, interaction: discord.Interaction):
        class PrizeModal(discord.ui.Modal):
            def __init__(self, parent_view):
                super().__init__(title="Giveaway Preis festlegen")
                self.parent_view = parent_view
                
                self.add_item(discord.ui.InputText(
                    label="Was wird verlost?",
                    placeholder="z.B. Discord Nitro, Game Key, etc.",
                    required=True,
                    max_length=256
                ))

            async def callback(self, interaction: discord.Interaction):
                self.parent_view.prize = self.children[0].value
                await interaction.response.send_message(
                    embed=create_embed(f"✅ Preis gesetzt: {self.parent_view.prize}", color=C.success_color),
                    ephemeral=True
                )

        modal = PrizeModal(self)
        await interaction.response.send_modal(modal)

    @discord.ui.button(
        label="Giveaway starten",
        style=discord.ButtonStyle.success,
        emoji="🎉"
    )
    async def start_giveaway_callback(self, button, interaction: discord.Interaction):
        if not self.selected_duration:
            await interaction.response.send_message(
                embed=create_embed("❌ Bitte wähle eine Giveaway-Dauer aus.", color=C.error_color),
                ephemeral=True
            )
            return
        
        if not self.prize:
            await interaction.response.send_message(
                embed=create_embed("❌ Bitte gib einen Preis ein.", color=C.error_color),
                ephemeral=True
            )
            return
        
        await create_giveaway(interaction, self.selected_duration, self.prize, self.winner_count, self.selected_role)
        self.stop()

    @discord.ui.button(
        label="Abbrechen",
        style=discord.ButtonStyle.secondary,
        emoji="❌"
    )
    async def cancel_callback(self, button, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed=create_embed("Giveaway abgebrochen.", color=C.warning_color),
            view=None
        )
        self.stop()


class GiveawayButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label=R.ticket_menu_giveaway,
            style=discord.ButtonStyle.primary,
            emoji="🎉",
            custom_id="ticket_menu_giveaway"
        )

    async def callback(self, interaction: discord.Interaction):
        embed = create_embed(
            "Konfiguriere dein Giveaway mit den Dropdown-Menüs und Buttons:",
            title="Giveaway erstellen",
            color=C.embed_color
        )
        embed.add_field(
            name="📋 Schritte",
            value="1. Dauer wählen\n2. Anzahl Gewinner wählen\n3. Rolle als Preis wählen (optional)\n4. Preis eingeben\n5. Giveaway starten",
            inline=False
        )
        view = GiveawayConfigView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        logger.info("Giveaway config menu opened", interaction)

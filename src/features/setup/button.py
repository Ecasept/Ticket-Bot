"""
Setup button interface for the ticket menu.
"""
import discord
from src.res import R, C
from src.utils import create_embed, logger
from src.database import db
from src.features.setup.setup import (
    setup_tickets, setup_transcript, setup_logchannel, 
    setup_timeout_logchannel, show_modroles
)


class SetupOptionView(discord.ui.View):
    def __init__(self, option):
        super().__init__(timeout=300)
        self.option = option

    @discord.ui.button(
        label=R.setup_view_value,
        style=discord.ButtonStyle.secondary,
        emoji="👁️"
    )
    async def view_value_callback(self, button, interaction: discord.Interaction):
        if self.option == "tickets":
            await setup_tickets(interaction)
        elif self.option == "transcript":
            await setup_transcript(interaction)
        elif self.option == "logchannel":
            await setup_logchannel(interaction)
        elif self.option == "timeout_logchannel":
            await setup_timeout_logchannel(interaction)
        elif self.option == "modroles":
            await show_modroles(interaction)
        
        logger.info(f"Viewed setup option {self.option}", interaction)

    @discord.ui.button(
        label=R.setup_set_value,
        style=discord.ButtonStyle.primary,
        emoji="✏️"
    )
    async def set_value_callback(self, button, interaction: discord.Interaction):
        if self.option == "tickets":
            await self._set_tickets(interaction)
        elif self.option == "transcript":
            await self._set_transcript(interaction)
        elif self.option == "logchannel":
            await self._set_logchannel(interaction)
        elif self.option == "timeout_logchannel":
            await self._set_timeout_logchannel(interaction)
        elif self.option == "modroles":
            await self._set_modroles(interaction)
        
        logger.info(f"Setting setup option {self.option}", interaction)

    async def _set_tickets(self, interaction: discord.Interaction):
        class CategorySelectView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=120)

            @discord.ui.channel_select(
                placeholder="Wähle eine Kategorie für Tickets",
                channel_types=[discord.ChannelType.category]
            )
            async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
                category = select.values[0]
                await setup_tickets(interaction, category)
                self.stop()

        view = CategorySelectView()
        await interaction.response.send_message(
            embed=create_embed("Wähle eine Kategorie für Tickets:", title="Tickets Kategorie setzen"),
            view=view,
            ephemeral=True
        )

    async def _set_transcript(self, interaction: discord.Interaction):
        class CategorySelectView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=120)

            @discord.ui.channel_select(
                placeholder="Wähle eine Kategorie für Transcripts",
                channel_types=[discord.ChannelType.category]
            )
            async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
                category = select.values[0]
                await setup_transcript(interaction, category)
                self.stop()

        view = CategorySelectView()
        await interaction.response.send_message(
            embed=create_embed("Wähle eine Kategorie für Transcripts:", title="Transcript Kategorie setzen"),
            view=view,
            ephemeral=True
        )

    async def _set_logchannel(self, interaction: discord.Interaction):
        class ChannelSelectView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=120)

            @discord.ui.channel_select(
                placeholder="Wähle einen Log-Channel",
                channel_types=[discord.ChannelType.text]
            )
            async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
                channel = select.values[0]
                await setup_logchannel(interaction, channel)
                self.stop()

        view = ChannelSelectView()
        await interaction.response.send_message(
            embed=create_embed("Wähle einen Log-Channel:", title="Log Channel setzen"),
            view=view,
            ephemeral=True
        )

    async def _set_timeout_logchannel(self, interaction: discord.Interaction):
        class ChannelSelectView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=120)

            @discord.ui.channel_select(
                placeholder="Wähle einen Timeout Log-Channel",
                channel_types=[discord.ChannelType.text]
            )
            async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
                channel = select.values[0]
                await setup_timeout_logchannel(interaction, channel)
                self.stop()

        view = ChannelSelectView()
        await interaction.response.send_message(
            embed=create_embed("Wähle einen Timeout Log-Channel:", title="Timeout Log Channel setzen"),
            view=view,
            ephemeral=True
        )

    async def _set_modroles(self, interaction: discord.Interaction):
        class ModRolesSelectView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=120)
                self.selected_roles = []

            @discord.ui.role_select(
                placeholder=R.setup_modroles_select_placeholder,
                min_values=1,
                max_values=25,
            )
            async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
                self.selected_roles = select.values
                await interaction.response.defer()

            @discord.ui.button(
                label=R.modroles_submit_button_label,
                style=discord.ButtonStyle.primary,
            )
            async def submit_callback(self, button, interaction: discord.Interaction):
                if not self.selected_roles:
                    await interaction.response.send_message(embed=create_embed(R.setup_modroles_none_selected, color=C.error_color), ephemeral=True)
                    return
                # Save selected roles as comma-separated IDs
                role_ids = [str(role.id) for role in self.selected_roles]
                db.set_constant(C.mod_roles, ",".join(role_ids), interaction.guild.id)
                roles_mentions = ", ".join([role.mention for role in self.selected_roles])
                await interaction.response.edit_message(
                    embed=create_embed(R.setup_modroles_set % roles_mentions,
                                     color=C.success_color, title=R.mod_roles_title),
                    view=None
                )
                self.stop()

        view = ModRolesSelectView()
        await interaction.response.send_message(
            embed=create_embed(R.setup_modroles_select_prompt, title=R.mod_roles_title),
            view=view,
            ephemeral=True
        )


class SetupSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.select(
        placeholder="Wähle eine Setup-Option",
        options=[
            discord.SelectOption(
                label="Tickets Kategorie",
                description="Kategorie für Tickets setzen/anzeigen",
                value="tickets",
                emoji="🎫"
            ),
            discord.SelectOption(
                label="Transcript Kategorie", 
                description="Kategorie für Transcripts setzen/anzeigen",
                value="transcript",
                emoji="📜"
            ),
            discord.SelectOption(
                label="Log Channel",
                description="Log Channel setzen/anzeigen",
                value="logchannel",
                emoji="📝"
            ),
            discord.SelectOption(
                label="Timeout Log Channel",
                description="Timeout Log Channel setzen/anzeigen", 
                value="timeout_logchannel",
                emoji="⏰"
            ),
            discord.SelectOption(
                label="Moderator Rollen",
                description="Moderator Rollen setzen/anzeigen",
                value="modroles",
                emoji="👮"
            )
        ]
    )
    async def setup_select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        option = select.values[0]
        
        # Show the new interface with Set Value and View Value buttons
        option_names = {
            "tickets": "Tickets Kategorie",
            "transcript": "Transcript Kategorie", 
            "logchannel": "Log Channel",
            "timeout_logchannel": "Timeout Log Channel",
            "modroles": "Moderator Rollen"
        }
        
        embed = create_embed(
            f"Was möchtest du mit **{option_names[option]}** machen?",
            title="Setup Option",
            color=C.embed_color
        )
        view = SetupOptionView(option)
        await interaction.response.edit_message(embed=embed, view=view)
        
        logger.info(f"Setup option {option} selected", interaction)


class SetupButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label=R.ticket_menu_setup,
            style=discord.ButtonStyle.secondary,
            emoji="⚙️",
            custom_id="ticket_menu_setup"
        )

    async def callback(self, interaction: discord.Interaction):
        embed = create_embed(
            "Wähle eine Setup-Option aus dem Dropdown-Menü:",
            title="Bot Setup",
            color=C.embed_color
        )
        view = SetupSelectView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        logger.info("Setup select menu opened", interaction)

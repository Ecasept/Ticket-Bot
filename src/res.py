"""
String resources and constants for the Discord bot, supporting localization and configuration.
"""
# String resources

from dataclasses import dataclass
import discord


def get_resources(lang: str):
    """
    Return the resource class for the specified language.
    Args:
        lang (str): Language code (e.g., 'de').
    Returns:
        ResDE: The resource class for German.
    Raises:
        ValueError: If the language is not supported.
    """
    if lang == "de":
        return ResDE()
    else:
        raise ValueError(f"Language '{lang}' not supported.")


@dataclass
class ResDE:
    """
    German string resources for the bot's UI and messages.
    """
    error_title: str = "Fehler"
    panel_msg: str = "Drücke den Button um ein Ticket zu erstellen."
    create_ticket_button: str = "Ticket erstellen"
    ticket_msg_created: str = "Benutzer können den Knopf unten benutzten um Tickets zu erstellen!"
    create_ticket_emoji: str = "✉️"
    ticket_panel_title: str = "Ticket Support"

    ticket_msg_desc: str = "Erstelle eine Nachricht mit einem Knopf um ein Ticket zu erstellen."
    ticket_channel_created: str = "Ticket erstellt! %s"
    ticket: str = "ticket"

    ping_desc: str = "Testet ob der Bot antwortet."

    close_ticket: str = "Ticket schließen"
    ticket_closed_msg: str = "Dein Ticket wurde geschlossen, %s!"

    ticket_category_title: str = "Erstelle ein Ticket"
    ticket_category_placeholder: str = "Wähle eine Kategorie"

    application: str = "Bewerbung"
    report: str = "Report"
    support: str = "Support"
    application_prefix: str = "bewerbung"
    report_prefix: str = "report"
    support_prefix: str = "support"
    application_desc: str = "Neue Bewerbung einreichen"
    report_desc: str = "Einen Nutzer melden"
    support_desc: str = "Hilfe bei allgemeinen Fragen"

    choose_category: str = "Wähle eine Kategorie für dein Ticket."

    assign_ticket: str = "Annehmen"
    unassign_ticket: str = "Freigeben"

    mod_options: str = "Moderator-Optionen"
    mod_options_no_permission: str = "Du hast keine Berechtigung um diese Optionen zu sehen."
    mod_options_assigned_msg: str = "Dieses Ticket ist an %s zugewiesen."
    mod_options_unassigned_msg: str = "Dieses Ticket ist nicht zugewiesen."

    approve_application: str = "Annehmen"
    reject_application: str = "Ablehnen"

    close_ticket_request_title: str = "Ticket schließen?"

    header_msg_application: str = "Willkommen im Ticket, %s! Hier kannst du deine Bewerbung einreichen"
    header_msg_report: str = "Willkommen im Ticket, %s! Hier kannst du deinen Report einreichen"
    header_msg_support: str = "Willkommen im Ticket, %s! Hier kannst du deine Support-Anfrage stellen"

    ticket_not_found_msg: str = "Ticket nicht gefunden. Bitte erstelle ein neues Ticket."

    user_not_found_msg: str = "Benutzer nicht gefunden. Bitte erstelle ein neues Ticket."
    application_approved_msg: str = "Herzlichen Glückwunsch, %s! Du bist jetzt ein Mitglied des Support-Teams."
    application_rejected_msg: str = "Leider wurde deine Bewerbung abgelehnt, %s."

    continue_button: str = "Weiter"

    ticket_not_found: str = "Dieses Ticket konnte nicht in der Datenbank gefunden werden."
    ticket_already_closed: str = "Dieses Ticket ist bereits geschlossen."
    ticket_close_no_permission: str = "Du hast keine Berechtigung um dieses Ticket zu schließen."

    ticket_close_request_msg: str = "%s möchte dieses Ticket schließen."
    ticket_close_request_accept: str = "Annehmen"
    ticket_close_request_decline: str = "Ablehnen"
    ticket_close_request_declined_msg: str = "%s, deine Anfrage das Ticket zu schließen wurde abgelehnt."
    ticket_close_request_decline_no_permission: str = "Du hast keine Berechtigung diese Anfrage abzulehnen."
    ticket_close_request_accept_no_permission: str = "Du hast keine Berechtigung diese Anfrage anzunehmen."

    delete_ticket_button: str = "Löschen"
    reopen_ticket_button: str = "Wieder öffnen"
    ticket_delete_no_permission: str = "Du hast keine Berechtigung dieses Ticket zu löschen."
    ticket_reopen_no_permission: str = "Du hast keine Berechtigung dieses Ticket wieder zu öffnen."
    ticket_reopened_msg: str = "%s, dein Ticket wurde wieder geöffnet."

    # setup.py
    setup_title: str = "Setup"
    setup_subcommand_desc = "Konfiguriert den Bot."

    # setup_tickets
    setup_tickets_desc = "Die Kategorie, in der Tickets erstellt werden sollen."
    setup_no_ticket_category = "Es ist derzeit keine Kategorie für Tickets festgelegt."
    setup_tickets_current_category = "Die aktuelle Ticket-Kategorie ist %s."
    setup_tickets_set_category = "Die Ticket-Kategorie wurde auf %s gesetzt."
    setup_ticket_category_not_found = "Die Kategorie für Tickets konnte nicht gefunden werden. Bitte stelle sicher, dass die Kategorie existiert und der Bot die Berechtigung hat, sie zu sehen."

    # setup_transcript
    setup_transcript_desc = "Die Kategorie, in der Transkripte gespeichert werden sollen."
    setup_no_transcript_category = "Es ist derzeit keine Kategorie für Transkripte festgelegt."
    setup_transcript_current_category = "Die aktuelle Transkript-Kategorie ist %s."
    setup_transcript_set_category = "Die Transkript-Kategorie wurde auf %s gesetzt."
    setup_transcript_category_not_found = "Die Kategorie für Transkripte konnte nicht gefunden werden. Bitte stelle sicher, dass die Kategorie existiert und der Bot die Berechtigung hat, sie zu sehen."


@dataclass
class Constants:
    """
    Constants for the bot, such as category names, role names, and colors.
    """
    support_role_name: str = "Support"
    ticket_category: str = "ticket_category"
    transcript_category: str = "transcript_category"
    db_file: str = "db/tickets.db"
    db_schema_file: str = "db/schema.sql"

    cat_application: str = "application"
    cat_report: str = "report"
    cat_support: str = "support"

    # Embed colors
    embed_color: discord.Color = discord.Color.blue()
    success_color: discord.Color = discord.Color.green()
    error_color: discord.Color = discord.Color.red()
    warning_color: discord.Color = discord.Color.orange()

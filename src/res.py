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
    error_occurred: str = "Ein Fehler ist aufgetreten: %s"

    panel_msg: str = "Drücke den Button um ein Ticket zu erstellen. Du kannst danach eine Kategorie auswählen."
    create_ticket_button: str = "Ticket erstellen"
    ticket_msg_created: str = "Benutzer können den Knopf unten benutzten um Tickets zu erstellen!"
    create_ticket_emoji: str = "✉️"
    ticket_panel_title: str = "Ticket Support"

    ticket_msg_desc: str = "Erstelle eine Nachricht mit einem Knopf um ein Ticket zu erstellen."
    ticket_channel_created: str = "Ticket erstellt! %s"
    ticket: str = "ticket"

    ping_desc: str = "Testet ob der Bot antwortet."

    close_ticket: str = "Ticket schließen"
    ticket_closed_msg: str = "Das Ticket wurde von %s geschlossen."

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

    mod_options_title: str = "Moderator-Optionen"
    mod_options_no_permission: str = "Du hast keine Berechtigung diese Optionen zu benutzen."
    mod_options_user: str = "Ersteller"
    mod_options_assignee: str = "Zugewiesen an"
    mod_options_unassigned: str = "Nicht zugewiesen"
    mod_options_category: str = "Kategorie"
    mod_options_created_at: str = "Erstellt am"
    mod_options_archived: str = "Archiviert"
    mod_options_archived_yes: str = "Ja"
    mod_options_archived_no: str = "Nein"

    approve_application: str = "Annehmen"
    reject_application: str = "Ablehnen"

    close_ticket_request_title: str = "Ticket schließen?"

    header_msg_application: str = "Willkommen im Ticket, %s! Hier kannst du deine Bewerbung einreichen"
    header_msg_report: str = "Willkommen im Ticket, %s! Hier kannst du jemanden melden"
    header_msg_support: str = "Willkommen im Ticket, %s! Hier kannst du deine Support-Anfrage stellen"
    header_title_support: str = "Ticket-Support"
    header_title_application: str = "Bewerbung"
    header_title_report: str = "Report"
    header_footer: str = "Ticket-ID: %s"

    ticket_not_found_msg: str = "Ticket nicht gefunden. Bitte erstelle ein neues Ticket."

    user_not_found_msg: str = "Ersteller nicht gefunden. Bitte erstelle ein neues Ticket."
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
    ticket_reopened_msg: str = "Das Ticket wurde wieder geöffnet von %s."

    ticket_assigned_msg: str = "Das Ticket wurde an %s zugewiesen."
    ticket_unassigned_msg: str = "Das Ticket wurde freigegeben."

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

    # Setup Log Channel
    setup_logchannel_desc: str = "Konfiguriert den Log-Channel für Team-Aktionen."
    setup_no_logchannel: str = "Es ist kein Log-Channel für Team-Aktionen konfiguriert."
    setup_logchannel_not_found: str = "Der konfigurierte Log-Channel wurde nicht gefunden."
    setup_logchannel_current: str = "Der aktuelle Log-Channel für Team-Aktionen ist %s."
    setup_logchannel_set: str = "Der Log-Channel für Team-Aktionen wurde auf %s gesetzt."
    log_channel_title: str = "Team Log Channel"

    # Setup Mod Roles (multiple)
    setup_modroles_desc: str = "Konfiguriert die Moderator-Rollen (mehrere auswählbar)."
    setup_modroles_select_prompt: str = "Bitte wähle die Moderator-Rollen aus."
    setup_modroles_select_placeholder: str = "Moderator-Rollen auswählen"
    setup_modroles_set: str = "Die Moderator-Rollen wurden auf %s gesetzt."
    setup_modroles_none_selected: str = "Bitte wähle mindestens eine Rolle aus."
    setup_modroles_current: str = "Die aktuellen Moderator-Rollen sind: %s."
    mod_roles_title: str = "Moderator Rollen"
    setup_no_modroles: str = "Es sind keine Moderator-Rollen konfiguriert."
    setup_modroles_not_found: str = "Eine oder mehrere konfigurierte Moderator-Rollen wurden nicht gefunden."
    modroles_submit_button_label: str = "Auswählen"

    # Team Commands
    team_group_desc: str = "Verwaltet Team-Mitglieder und Listen."
    team_add_desc: str = "Fügt einen Benutzer zu einem Team hinzu und weist eine Rolle zu."
    team_add_success_log: str = "%s wurde von %s die Rolle %s zugewiesen."
    team_add_no_log_channel: str = "Fehler: Bitte konfiguriere zuerst einen Log-Channel mit `/setup logchannel`."
    team_list_desc: str = "Listet Team-Mitglieder basierend auf ausgewählten Rollen auf."
    team_list_select_roles_prompt: str = "Bitte wähle die Rollen aus, die als Team-Rollen angezeigt werden sollen."
    team_list_role_select_placeholder: str = "Wähle Rollen aus"
    team_list_submit_button_label: str = "Anzeigen"
    team_list_embed_title: str = "Team-Mitglieder"
    team_list_no_members_found: str = "Keine Mitglieder mit diesen Rollen als höchste Berechtigung gefunden."
    team_list_select_at_least_one_role: str = "Bitte wähle mindestens eine Rolle aus."
    add_role_no_perm: str = "Du hast keine Berechtigung, diese Rolle zuzuweisen."
    new_team_member_title: str = "Neues Team-Mitglied"

    # Team command option descriptions
    team_add_user_desc: str = "Der Benutzer, der zum Team hinzugefügt werden soll."
    team_add_role_desc: str = "Die Rolle, die dem Benutzer zugewiesen werden soll."

    # Application
    application_cancelled: str = "Die Bewerbung wurde abgebrochen."
    application_info: str = "Bitte gib die Informationen für deine Bewerbung ein."
    application_age_label: str = "Alter"
    application_age_placeholder: str = "Gib dein Alter ein"
    application_apply_for_label: str = "Für was möchtest du dich bewerben?"
    application_apply_for_placeholder: str = "Z.B. Moderator, Entwickler"
    application_text_label: str = "Bewerbungstext"
    application_text_placeholder: str = "Schreibe hier deine Bewerbung..."


@dataclass
class Constants:
    """
    Constants for the bot, such as category names, role names, and colors.
    """
    support_role_name: str = "Support"
    ticket_category: str = "ticket_category"
    transcript_category: str = "transcript_category"
    mod_roles: str = "mod_role_ids"
    log_channel: str = "log_channel_id"  # Key for the log channel in DB
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

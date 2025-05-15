# String resources

from dataclasses import dataclass


def get_resources(lang: str):
    if lang == "de":
        return ResDE()
    else:
        raise ValueError(f"Language '{lang}' not supported.")


@dataclass
class ResDE:
    panel_msg: str = "Drücke den Button um ein Ticket zu erstellen."
    create_ticket_button: str = "Ticket erstellen"
    ticket_msg_created: str = "Benutzer können den Knopf unten benutzten um Tickets zu erstellen!"
    create_ticket_emoji: str = "✉️"

    ticket_msg_desc: str = "Erstelle eine Nachricht mit einem Knopf um ein Ticket zu erstellen."
    ticket_channel_created: str = "Ticket-Kanal erstellt! %s"
    ticket: str = "ticket"

    ping_desc: str = "Testet ob der Bot antwortet."

    close_ticket: str = "Ticket schließen"
    ticket_closed_msg: str = "Dieses Ticket wurde geschlossen. Du kannst es nicht mehr benutzen."

    ticket_category_title: str = "Erstelle ein Ticket"
    ticket_category_placeholder: str = "Wähle eine Kategorie"

    application: str = "Bewerbung"
    report: str = "Report"
    application_prefix: str = "bewerbung"
    report_prefix: str = "report"
    application_desc: str = "Neue Bewerbung einreichen"
    report_desc: str = "Einen Nutzer melden"

    choose_category: str = "Wähle eine Kategorie für dein Ticket."

    assign_ticket: str = "Annehmen"
    unassign_ticket: str = "Freigeben"

    mod_options: str = "Moderator-Optionen"
    mod_options_no_permission: str = "Du hast keine Berechtigung um diese Optionen zu sehen."
    mod_options_assigned_msg: str = "Dieses Ticket ist an %s zugewiesen."
    mod_options_unassigned_msg: str = "Dieses Ticket ist nicht zugewiesen."

    approve_application: str = "Annehmen"
    reject_application: str = "Ablehnen"

    header_msg_application: str = "Willkommen im Ticket, %s! Hier kannst du deine Bewerbung einreichen"
    header_msg_report: str = "Willkommen im Ticket, %s! Hier kannst du deinen Report einreichen"

    ticket_not_found_msg: str = "Ticket nicht gefunden. Bitte erstelle ein neues Ticket."

    user_not_found_msg: str = "Benutzer nicht gefunden. Bitte erstelle ein neues Ticket."
    application_approved_msg: str = "Herzlichen Glückwunsch, %s! Du bist jetzt ein Mitglied des Support-Teams."
    application_rejected_msg: str = "Leider wurde deine Bewerbung abgelehnt, %s."


@dataclass
class Constants:
    support_category_name: str = "Support"
    support_role_name: str = "Support"
    transcript_category_name: str = "Archiv"
    db_file: str = "db/tickets.db"
    db_schema_file: str = "db/schema.sql"

    cat_application: str = "application"
    cat_report: str = "report"

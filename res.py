# String resources

from dataclasses import dataclass


def get_resources(lang: str):
    if lang == "de":
        return ResDE()
    else:
        raise ValueError(f"Language '{lang}' not supported.")


@dataclass
class ResDE:
    create_ticket_msg: str = "Drücke den Button um ein Ticket zu erstellen."
    create_ticket_button: str = "Ticket erstellen"
    ticket_msg_created: str = "Benutzer können den Knopf unten benutzten um Tickets zu erstellen!"
    create_ticket_emoji: str = "✉️"

    ticket_msg_desc: str = "Erstelle eine Nachricht mit einem Knopf um ein Ticket zu erstellen."
    ticket_channel_created: str = "Ticket-Kanal erstellt!"
    ticket: str = "ticket"

    ping_desc: str = "Testet ob der Bot online ist."


@dataclass
class Constants:
    support_category_name: str = "Support"
    support_role_name: str = "Support"

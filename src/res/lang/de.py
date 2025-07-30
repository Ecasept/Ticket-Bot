from dataclasses import dataclass

from src.constants import C


@dataclass
class ResDE:
    """
    German string resources for the bot's UI and messages.
    """
    bot_activity: str = "auf /help"

    error_title: str = "Fehler"
    error_occurred: str = "Ein Fehler ist aufgetreten: %s"

    user_id_invalid: str = "Die Benutzer-ID ist ungültig."
    user_not_found: str = "Der Benutzer <@%s> konnte nicht auf dem Server gefunden werden."

    panel_msg: str = "Wähle eine Kategorie um ein Ticket zu erstellen."
    create_ticket_button: str = "Ticket erstellen"
    ticket_msg_created: str = "Benutzer können den Knopf unten benutzten um Tickets zu erstellen!"
    ticket_panel_title: str = "Ticket Support"

    application_emoji: str = "📝"
    support_emoji: str = "🛠️"
    report_emoji: str = "🚨"

    delete_emoji: str = "⛔"
    reopen_emoji: str = "🔄"

    close_emoji: str = "🔒"  # not an x because the bg of the button is red
    mod_options_emoji: str = "⚙️"

    invalid_duration: str = "❌ Ungültige Dauer `%s`. Nutze z.B. `10s`, `1m`, `2h`."

    ticket_channel_created: str = "Ticket erstellt! %s"
    ticket: str = "ticket"

    ping_response: str = "Pong!"

    # Ticket menu
    ticket_menu_title: str = "Ticket Menü"
    ticket_menu_description: str = "Wähle eine Option aus den verfügbaren Ticket-Befehlen:"
    ticket_menu_giveaway: str = "Giveaway"
    ticket_menu_timeout: str = "Timeout"
    ticket_menu_setup: str = "Setup"
    ticket_menu_giveaway_desc: str = "Starte ein Giveaway"
    ticket_menu_timeout_desc: str = "Benutzer timeout geben"
    ticket_menu_setup_desc: str = "Bot-Einstellungen konfigurieren"

    # Setup button labels
    setup_set_value: str = "Wert setzen"
    setup_view_value: str = "Wert anzeigen"

    close_ticket: str = "Schließen"
    ticket_closed_msg: str = "Das Ticket wurde von %s geschlossen."

    ticket_category_title: str = "Erstelle ein Ticket"
    ticket_category_placeholder: str = "Wähle eine Kategorie"
    ticket_category_select_placeholder: str = "Wähle eine Ticket-Kategorie..."

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
    assign_emoji: str = "📥"
    unassign_ticket: str = "Freigeben"
    unassign_emoji: str = "📤"

    mod_options_title: str = "Mod-Optionen"
    mod_options_no_permission: str = "Du hast keine Berechtigung diese Optionen zu benutzen."
    mod_options_user: str = "Ersteller"
    mod_options_assignee: str = "Zugewiesen an"
    mod_options_unassigned: str = "Nicht zugewiesen"
    mod_options_category: str = "Kategorie"
    mod_options_created_at: str = "Erstellt am"
    mod_options_archived: str = "Archiviert"
    mod_options_archived_yes: str = "Ja"
    mod_options_archived_no: str = "Nein"
    noch_fragen_label: str = "Noch Fragen?"
    noch_fragen_emoji: str = "❓"

    approve_application: str = "Bewerbung annehmen"
    approve_application_emoji: str = "✅"
    reject_application: str = "Bewerbung ablehnen"
    reject_application_emoji: str = "⛔"

    # Application rejection modal
    reject_application_modal_title: str = "Bewerbung ablehnen"
    reject_application_reason_label: str = "Grund für die Ablehnung"
    reject_application_reason_placeholder: str = "Gib einen Grund an (optional)"
    application_rejected_with_reason_msg: str = "%s, deine Bewerbung wurde aus folgendem Grund abgelehnt: %s"
    application_rejected_msg: str = "%s, deine Bewerbung wurde abgelehnt."

    close_ticket_request_title: str = "Ticket schließen?"

    header_msg_application: str = "Willkommen im Ticket, %s! Hier kannst du deine Bewerbung einreichen"
    header_msg_report: str = "Willkommen im Ticket, %s! Hier kannst du jemanden melden"
    header_msg_support: str = "Willkommen im Ticket, %s! Hier kannst du deine Support-Anfrage stellen"
    header_title_support: str = "Ticket-Support"
    header_title_application: str = "Bewerbung"
    header_title_report: str = "Report"
    header_footer: str = "Ticket-ID: %s"

    ticket_not_found_msg: str = "Ticket nicht gefunden. Bitte erstelle ein neues Ticket."

    application_approved_msg: str = "Herzlichen Glückwunsch, %s! Deine Bewerbung wurde angenommen."
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

    # Giveaway strings
    giveaway_desc: str = "Starte ein Giveaway mit automatischer Gewinnermittlung."
    giveaway_duration_desc: str = "Dauer des Giveaways (z.B. 30s, 2m, 1h)"
    giveaway_prize_desc: str = "Was wird verlost?"
    giveaway_winners_desc: str = "Anzahl der Gewinner"
    giveaway_role_desc: str = "Rolle die Gewinner erhalten (optional)"

    giveaway_duration_extreme: str = "❌ Dauer muss zwischen 10 Sekunden und 30 Tagen liegen."
    giveaway_invalid_winners: str = "❌ Ungültige Gewinner-Anzahl. Muss zwischen 1 und 20 sein."
    giveaway_started: str = "✅ Giveaway wurde gestartet!"
    giveaway_title: str = "🎉 Giveaway: %s"
    giveaway_description: str = "**%s** wird verlost!\n🏆 **%s** Gewinner werden ausgewählt"
    giveaway_ends_at: str = "🕐 Endet am"
    giveaway_role_prize: str = "🎭 Zusätzliche Rolle"
    giveaway_participation: str = "📝 Teilnahme"
    giveaway_react_to_participate: str = "Reagiere mit %s um teilzunehmen!"
    giveaway_footer: str = "Veranstaltet von Benutzer-ID: %s"
    giveaway_prize: str = "**Preis:** %s"
    giveaway_duration: str = "**Dauer:** %s"
    giveaway_role: str = "**Rolle:** %s"
    giveaway_host: str = "Veranstaltet von: %s"
    giveaway_winner_count: str = "Gewinner: %s"

    giveaway_winners_announcement: str = "🎊 Glückwunsch %s! Du hast **%s** gewonnen!"
    giveaway_no_participants: str = "Keiner hat das Giveaway gewonnen, da niemand teilgenommen hat."
    giveaway_ended_title: str = "🎉 Giveaway beendet"
    giveaway_role_awarded: str = "✅ Rolle %s wurde an die Gewinner vergeben."
    giveaway_role_perms_error: str = "⚠️ Konnte %s nicht an %s vergeben (fehlende Rechte)."
    giveaway_not_found: str = "Giveaway nicht in der Datenbank gefunden."
    giveaway_already_ended: str = "Dieses Giveaway ist bereits beendet."
    giveaway_no_role: str = "Keine Rolle"

    # setup.py
    setup_title: str = "Setup"
    setup_no_ticket_category = "Es ist derzeit keine Kategorie für Tickets festgelegt."
    setup_tickets_current_category = "Die aktuelle Ticket-Kategorie ist %s."
    setup_tickets_set_category = "Die Ticket-Kategorie wurde auf %s gesetzt."
    setup_ticket_category_not_found = "Die Kategorie für Tickets konnte nicht gefunden werden. Bitte stelle sicher, dass die Kategorie existiert und der Bot die Berechtigung hat, sie zu sehen."

    # setup_transcript
    setup_no_transcript_category = "Es ist derzeit keine Kategorie für Transkripte festgelegt."
    setup_transcript_current_category = "Die aktuelle Transkript-Kategorie ist %s."
    setup_transcript_set_category = "Die Transkript-Kategorie wurde auf %s gesetzt."
    setup_transcript_category_not_found = "Die Kategorie für Transkripte konnte nicht gefunden werden. Bitte stelle sicher, dass die Kategorie existiert und der Bot die Berechtigung hat, sie zu sehen."

    # Setup Log Channel
    setup_no_logchannel: str = "Es ist kein Log-Channel für Team-Aktionen konfiguriert."
    setup_logchannel_not_found: str = "Der konfigurierte Log-Channel wurde nicht auf diesem Server gefunden. Bitte stelle sicher, dass der Channel existiert und der Bot die Berechtigung hat, ihn zu sehen."
    setup_logchannel_current: str = "Der aktuelle Log-Channel für Team-Aktionen ist %s."
    setup_logchannel_set: str = "Der Log-Channel für Team-Aktionen wurde auf %s gesetzt."
    log_channel_title: str = "Team Log Channel"

    # Setup Mod Roles (multiple)
    setup_modroles_select_prompt: str = "Bitte wähle die Moderator-Rollen aus."
    setup_modroles_select_placeholder: str = "Moderator-Rollen auswählen"
    setup_modroles_set: str = "Die Moderator-Rollen wurden auf %s gesetzt."
    setup_modroles_none_selected: str = "Bitte wähle mindestens eine Rolle aus."
    setup_modroles_current: str = "Die aktuellen Moderator-Rollen sind: %s."
    mod_roles_title: str = "Moderator Rollen"
    setup_no_modroles: str = "Es sind keine Moderator-Rollen konfiguriert."
    setup_modroles_not_found: str = "Eine oder mehrere konfigurierte Moderator-Rollen konnten nicht auf dem Server gefunden werden. Bitte stelle sicher, dass die Rollen existieren und der Bot die Berechtigung hat, sie zu sehen."
    modroles_submit_button_label: str = "Auswählen"
    setup_modroles_invalid: str = "Eine oder mehrere ausgewählte Mod-Rollen sind ungültig. Bitte wähle gültige Rollen aus."

    # Team Commands
    team_add_success_log: str = "%s wurde von %s die Rolle %s zugewiesen."
    team_add_no_log_channel: str = "Fehler: Bitte konfiguriere zuerst einen Log-Channel mit `/setup logchannel`."
    team_list_select_roles_prompt: str = "Bitte wähle die Rollen aus, die als Team-Rollen angezeigt werden sollen."
    team_list_role_select_placeholder: str = "Wähle Rollen aus"
    team_list_submit_button_label: str = "Anzeigen"
    team_list_embed_title: str = "Team-Mitglieder"
    team_list_no_members_found: str = "Keine Mitglieder mit dieser Rolle gefunden."
    team_list_update_button_label: str = "Aktualisieren"
    team_list_upate_emoji: str = "🔄"
    team_list_select_at_least_one_role: str = "Bitte wähle mindestens eine Rolle aus."
    team_list_old_version: str = "Diese Team-Liste wurde mit einer älteren Version des Bots erstellt. Bitte lösche sie und erstelle eine neue."
    status_online: str = "🟢"
    status_idle: str = "🟡"
    status_dnd: str = "⛔"
    status_offline: str = "⚫"
    status_unknown: str = "❓"
    status_mobile: str = "📱"
    add_role_no_perm: str = "Der Bot hat keine Berechtigung um auf diese Rolle zuzugreifen."
    new_team_member_title: str = "Neues Team-Mitglied"

    team_remove_success_log: str = "%s wurde von %s die Rolle %s entfernt."
    team_remove_no_log_channel: str = "Fehler: Bitte konfiguriere zuerst einen Log-Channel mit `/setup logchannel`."
    team_remove_success_title: str = "Team-Mitglied entfernt"
    team_remove_user_missing_role: str = "Der Benutzer hat diese Rolle nicht."

    team_welcome_no_channel: str = "Es ist kein Willkommens-Channel konfiguriert."
    team_welcome_current_channel: str = "Der aktuelle Willkommens-Channel ist %s."
    team_welcome_channel_set: str = "Der Willkommens-Channel wurde auf %s gesetzt."
    team_welcome_channel_not_found: str = "Der Willkommens-Channel konnte nicht gefunden werden."
    welcome_message: str = "Willkommen %s, du bist nun %s."

    team_wechsel_success_log: str = "%s wurde von %s von %s zu %s gewechselt."
    team_wechsel_success_title: str = "Team-Rolle gewechselt"
    team_wechsel_user_missing_from_role: str = "Der Benutzer hat die alte Rolle nicht."
    team_wechsel_user_already_has_to_role: str = "Der Benutzer hat die neue Rolle bereits."

    # Application
    application_cancelled: str = "Die Bewerbung wurde abgebrochen."
    application_info: str = "Bitte gib die Informationen für deine Bewerbung ein."
    application_age_label: str = "Alter"
    application_age_placeholder: str = "Gib dein Alter ein"
    application_apply_for_label: str = "Für was möchtest du dich bewerben?"
    application_apply_for_placeholder: str = "Z.B. Moderator, Entwickler"
    application_text_label: str = "Bewerbungstext"
    application_text_placeholder: str = "Schreibe hier deine Bewerbung..."

    # Noch Fragen functionality
    noch_fragen_msg: str = "Hast du noch Fragen? Falls nicht, wird dieses Ticket in %d Stunden automatisch geschlossen."
    noch_fragen_title: str = "Ticket wird geschlossen"
    no_questions: str = "Keine Fragen mehr"
    noch_fragen_delete_emoji: str = "✅"
    no_questions_cancel: str = "Ich habe noch Fragen"
    noch_fragen_cancel_emoji: str = "❓"
    noch_fragen_no_permission: str = "Nur der Ersteller kann die Fragen beantworten."
    ticket_noch_fragen_close_error_title: str = "Fehler beim automatischen Schließen"
    ticket_no_close_time: str = "Dieses Ticket ist nicht (mehr) für das automatische Schließen konfiguriert. Bitte schließe es manuell."
    noch_fragen_cancel_msg: str = "%s, Du kannst jetzt wieder Fragen stellen."
    noch_fragen_delete_msg: str = "Das Ticket wird jetzt gelöscht. Der Channel wird nicht mehr benutzbar sein."
    noch_fragen_closed_msg: str = "Das Ticket wurde automatisch geschlossen."

    # Help command
    help_desc: str = "Zeigt alle verfügbaren Bot-Befehle an."
    help_title: str = "🤖 Bot Hilfe"
    help_description: str = "Hier sind alle verfügbaren Befehle für diesen Bot:"
    help_general_commands: str = "📋 **Allgemeine Befehle**"
    help_setup_commands: str = "⚙️ **Setup Befehle** (Administrator erforderlich)"
    help_team_commands: str = "👥 **Team Befehle** (Administrator erforderlich)"
    help_tutorial_title: str = "🚀 **Erste Schritte**"
    help_tutorial_text: str = f"**Setup-Reihenfolge:**\n1️⃣ `/setup tickets` - Kategorie für neue Tickets festlegen\n2️⃣ `/setup transcript` - Kategorie für geschlossene Tickets festlegen\n3️⃣ `/setup modroles` - Moderator-Rollen auswählen\n4️⃣ `/setup logchannel` - Log-Channel für Team-Aktionen *(optional)*\n5️⃣ `/createpanel` - Ticket-Panel für User erstellen\n\n✨ **Tipp:** Deine Frage wurde nicht beantwortet? Erstelle auf unserem [Support-Server]({C.support_guild_invite_link}) ein Ticket!"
    help_footer: str = f"{C.bot_name} - Tickets & more"

    # Timeout
    timeout_success: str = "✅ %s wurde für %s getimeoutet. Grund: %s"
    timeout_success_no_reason: str = "✅ %s wurde für %s getimeoutet."
    timeout_dm_notification: str = "Du wurdest auf dem Server '%s' für %s getimeoutet. Grund: %s"
    timeout_dm_notification_no_reason: str = "Du wurdest auf dem Server '%s' für %s getimeoutet."
    timeout_log_title: str = "📛 Timeout"
    timeout_log_user: str = "👤 Nutzer"
    timeout_log_duration: str = "⏱ Dauer"
    timeout_log_reason: str = "📝 Grund"
    timeout_log_moderator: str = "👮 Durch"
    timeout_log_no_reason: str = "Kein Grund angegeben"
    timeout_invalid_duration: str = "❌ Ungültige Dauer. Nutze z.B. `1m`, `2h`, `3d`."
    timeout_duration_too_long: str = "❌ Dauer des Timeouts darf maximal 28 Tage betragen."
    timeout_cant_timeout_self: str = "❌ Du kannst dich nicht selbst timeouten."
    timeout_cant_timeout_bot: str = "❌ Du kannst den Bot nicht timeouten."
    timeout_failed: str = "❌ Timeout fehlgeschlagen: %s"
    setup_timeout_logchannel_desc: str = "Konfiguriert den Log-Channel für Timeouts."
    setup_no_timeout_logchannel: str = "Es ist kein Log-Channel für Timeouts konfiguriert."
    setup_timeout_logchannel_not_found: str = "Der konfigurierte Timeout-Log-Channel wurde nicht auf diesem Server gefunden."
    setup_timeout_logchannel_current: str = "Der aktuelle Timeout-Log-Channel ist %s."
    setup_timeout_logchannel_set: str = "Der Timeout-Log-Channel wurde auf %s gesetzt."
    timeout_log_channel_title: str = "Timeout Log Channel"

    # Application Ban
    team_sperre_desc: str = "Sperrt einen Benutzer von der Erstellung von Bewerbungstickets."
    team_sperre_user_desc: str = "Der Benutzer, der gesperrt werden soll."
    team_sperre_duration_desc: str = "Dauer der Sperre (z.B. 1d, 2w, 3m). Optional, Standard ist für immer."
    team_sperre_success: str = "✅ %s wurde von der Erstellung von Bewerbungstickets gesperrt."
    team_sperre_already_banned: str = "❌ %s ist bereits von der Erstellung von Bewerbungstickets gesperrt."

    team_sperre_unban: str = "Sperre aufheben"
    team_sperre_unban_emoji: str = "🔓"
    team_sperre_unban_success: str = "✅ %s wurde von der Sperre für Bewerbungstickets befreit."

    application_banned_message: str = "❌ Du bist von der Erstellung von Bewerbungstickets gesperrt und kannst keine neuen Bewerbungen einreichen."

    team_sperre_logging_failed_suffix: str = "\nDer Nutzer wurde trotzdem gesperrt."
    team_sperre_success_log_duration: str = "%s wurde von %s für `%s` von der Erstellung von Bewerbungstickets gesperrt."
    team_sperre_success_log: str = "%s wurde von %s von der Erstellung von Bewerbungstickets gesperrt."
    team_sperre_success_title: str = "Bewerbungssperre"
    team_sperre_unban_log: str = "%s hat die Sperre von %s für Bewerbungstickets aufgehoben."
    team_sperre_unban_log_title: str = "Bewerbungssperre aufgehoben"

    # Banlist
    banlist_group_desc: str = "Verwaltet die Banliste."
    banlist_show_desc: str = "Zeigt die aktuelle Banliste an."
    banlist_add_desc: str = "Fügt einen Benutzer zur Banliste hinzu."
    banlist_remove_desc: str = "Entfernt einen Benutzer von der Banliste."
    banlist_add_name_desc: str = "Der Name des zu bannenden Benutzers."
    banlist_add_reason_desc: str = "Der Grund für den Bann."
    banlist_add_banned_by_desc: str = "Wer hat den Benutzer gebannt."
    banlist_add_length_desc: str = "Die Dauer des Banns."
    banlist_remove_name_desc: str = "Der Name des zu entbannenden Benutzers."
    banlist_embed_title: str = "Banliste"
    banlist_no_bans: str = "Die Banliste ist leer."
    banlist_add_success: str = "✅ %s wurde zur Banliste hinzugefügt."
    banlist_add_failed: str = "❌ Konnte %s nicht zur Banliste hinzufügen: %s"
    banlist_remove_success: str = "✅ %s wurde von der Banliste entfernt."
    banlist_remove_failed: str = "❌ Konnte %s nicht von der Banliste entfernen: %s"
    banlist_already_banned: str = "❌ %s ist bereits auf der Banliste."
    banlist_not_banned: str = "❌ %s ist nicht auf der Banliste."
    banlist_item_banned_by_for: str = "Gebannt von **%s** für **%s**"
    banlist_item_reason: str = "Grund: %s"
    list_too_long: str = "Die Liste ist zu lang, um sie in einem Embed anzuzeigen."
    update_button_label: str = "Aktualisieren"

    banlist_no_image: str = "❌ %s hat kein Bild hinterlegt."
    banlist_image_indicator: str = " + Bild"
    banlist_invalid_url: str = "❌ Die angegebene URL ist ungültig. Bitte gib eine gültige HTTP/HTTPS-URL an."
    banlist_showimg_embed_title = "Bild von %s"

    # Category management strings
    category_new: str = "Neue Kategorie"
    category_edit: str = "Kategorie bearbeiten"
    category_delete: str = "Kategorie löschen"
    category_yes_delete: str = "Ja, löschen"
    category_cancel: str = "Abbrechen"
    category_save: str = "Speichern"
    category_name_label: str = "Name"
    category_name_placeholder: str = "Name der Kategorie"
    category_emoji_label: str = "Emoji"
    category_emoji_placeholder: str = "Emoji für die Kategorie"
    category_description_label: str = "Beschreibung"
    category_description_placeholder: str = "Beschreibung der Kategorie"
    category_name_emoji_desc: str = "Name/Emoji/Beschreibung"
    category_roles_permission: str = "Rollen-Berechtigung"
    category_questions: str = "Fragen"
    category_questions_count: str = "Fragen (%d)"
    category_select_label: str = "Kategorien"
    category_select_placeholder: str = "Wähle eine Kategorie zum Löschen..."
    category_roles_placeholder: str = "Rollen auswählen (leer = alle Benutzer)..."
    category_field_id: str = "ID"
    category_field_permission: str = "Berechtigung"
    category_field_all_users: str = "Alle Benutzer"
    category_field_no_questions: str = "Keine Fragen konfiguriert"
    category_field_no_description: str = "Keine Beschreibung"

    # Category creation
    category_create_name_placeholder: str = "z.B. Support, Bewerbung, Bug Report"
    category_create_emoji_placeholder: str = "z.B. 🎫, 📝, 🐛 (Unicode oder Discord Emoji)"
    category_create_description_placeholder: str = "Kurze Beschreibung der Kategorie"

    # Category questions
    category_question_label: str = "Frage"
    category_questions_all_label: str = "Fragen (eine pro Zeile)"
    category_question_add: str = "Frage hinzufügen"
    category_questions_replace_all: str = "Alle Fragen ersetzen"
    category_questions_delete_all: str = "Alle Fragen löschen"

    # Timeout interface strings
    timeout_user_select_placeholder: str = "Wähle einen Benutzer zum Timeout"
    timeout_duration_select_placeholder: str = "Wähle eine Timeout-Dauer"
    timeout_execute_button: str = "Timeout ausführen"
    timeout_cancel_button: str = "Abbrechen"
    timeout_30s_label: str = "30 Sekunden"
    timeout_30s_desc: str = "Kurzer Timeout"
    timeout_5m_label: str = "5 Minuten"
    timeout_5m_desc: str = "Standard Timeout"
    timeout_1h_label: str = "1 Stunde"
    timeout_1h_desc: str = "Längerer Timeout"
    timeout_1d_label: str = "1 Tag"
    timeout_1d_desc: str = "Täglicher Timeout"
    timeout_1w_label: str = "1 Woche"
    timeout_1w_desc: str = "Wöchentlicher Timeout"
    timeout_select_user_error: str = "❌ Bitte wähle einen Benutzer aus."
    timeout_select_duration_error: str = "❌ Bitte wähle eine Timeout-Dauer aus."
    timeout_user_not_on_server: str = "❌ Benutzer ist nicht auf diesem Server."
    timeout_cancelled: str = "Timeout abgebrochen."
    timeout_interface_title: str = "Benutzer Timeout"
    timeout_interface_description: str = "Wähle einen Benutzer und eine Timeout-Dauer aus den Dropdown-Menüs:"

    # Giveaway interface strings
    giveaway_duration_select_placeholder: str = "Wähle eine Giveaway-Dauer"
    giveaway_duration_30s_label: str = "30 Sekunden"
    giveaway_duration_30s_desc: str = "Test-Giveaway"
    giveaway_duration_5m_label: str = "5 Minuten"
    giveaway_duration_5m_desc: str = "Kurzes Giveaway"
    giveaway_duration_1h_label: str = "1 Stunde"
    giveaway_duration_1h_desc: str = "Standard Giveaway"
    giveaway_duration_1d_label: str = "1 Tag"
    giveaway_duration_1d_desc: str = "Tägliches Giveaway"
    giveaway_duration_1w_label: str = "1 Woche"
    giveaway_duration_1w_desc: str = "Wöchentliches Giveaway"

    giveaway_winner_count_select_placeholder: str = "Anzahl Gewinner wählen"
    giveaway_winner_1_label: str = "1 Gewinner"
    giveaway_winner_2_label: str = "2 Gewinner"
    giveaway_winner_3_label: str = "3 Gewinner"
    giveaway_winner_5_label: str = "5 Gewinner"
    giveaway_winner_10_label: str = "10 Gewinner"

    giveaway_role_select_placeholder: str = "Wähle eine Rolle als Preis (optional)"
    giveaway_set_prize_button: str = "Preis eingeben"
    giveaway_start_button: str = "Giveaway starten"
    giveaway_cancel_button: str = "Abbrechen"

    # Setup placeholders for selects
    setup_tickets_select_placeholder: str = "Wähle eine Kategorie für Tickets"
    setup_transcript_select_placeholder: str = "Wähle eine Kategorie für Transcripts"
    setup_logchannel_select_placeholder: str = "Wähle einen Log-Channel"
    setup_timeout_logchannel_select_placeholder: str = "Wähle einen Timeout Log-Channel"
    setup_select_option_placeholder: str = "Wähle eine Setup-Option"

    # Setup select option labels and descriptions
    setup_option_tickets_label: str = "Tickets Kategorie"
    setup_option_tickets_desc: str = "Kategorie für Tickets setzen/anzeigen"
    setup_option_transcript_label: str = "Transcript Kategorie"
    setup_option_transcript_desc: str = "Kategorie für Transkripte setzen/anzeigen"
    setup_option_logchannel_label: str = "Log Channel"
    setup_option_logchannel_desc: str = "Log Channel setzen/anzeigen"
    setup_option_timeout_logchannel_label: str = "Timeout Log Channel"
    setup_option_timeout_logchannel_desc: str = "Timeout Log Channel setzen/anzeigen"
    setup_option_modroles_label: str = "Moderator Rollen"
    setup_option_modroles_desc: str = "Moderator Rollen setzen/anzeigen"

    banlist_showimg_embed_title = "Bild von %s"

    # Category select default placeholder
    category_select_default_placeholder: str = "Kategorie wählen..."

    @dataclass
    class Feature:
        @dataclass
        class Giveaway:
            role_award_reason: str = "Bei einem Giveaway gewonnen"

            @dataclass
            class Button:
                config_embed_desc: str = "Konfiguriere dein Giveaway mit den Dropdown-Menüs und Buttons:"
                config_embed_title: str = "Giveaway erstellen"
                config_embed_steps_name: str = "📋 Schritte"
                config_embed_steps_value: str = "1. Dauer wählen\n2. Anzahl Gewinner wählen\n3. Rolle als Preis wählen (optional)\n4. Preis eingeben\n5. Giveaway starten"
                prize_set_success: str = "✅ Preis gesetzt: %s"
                no_duration_error: str = "❌ Bitte wähle eine Giveaway-Dauer aus."
                no_prize_error: str = "❌ Bitte gib einen Preis ein."
                cancelled_msg: str = "Giveaway abgebrochen."

                @dataclass
                class PrizeModal:
                    title: str = "Giveaway Preis festlegen"
                    label: str = "Was wird verlost?"
                    placeholder: str = "z.B. Discord Nitro, Game Key, etc."
                prize_modal = PrizeModal()
            button = Button()
        giveaway = Giveaway()

        @dataclass
        class Setup:
            @dataclass
            class Button:
                @dataclass
                class SetTickets:
                    embed_desc: str = "Wähle eine Kategorie für Tickets:"
                    embed_title: str = "Tickets Kategorie setzen"
                set_tickets = SetTickets()

                @dataclass
                class SetTranscript:
                    embed_desc: str = "Wähle eine Kategorie für Transcripts:"
                    embed_title: str = "Transcript Kategorie setzen"
                set_transcript = SetTranscript()

                @dataclass
                class SetLogChannel:
                    embed_desc: str = "Wähle einen Log-Channel:"
                    embed_title: str = "Log Channel setzen"
                set_logchannel = SetLogChannel()

                @dataclass
                class SetTimeoutLogChannel:
                    embed_desc: str = "Wähle einen Timeout Log-Channel:"
                    embed_title: str = "Timeout Log Channel setzen"
                set_timeout_logchannel = SetTimeoutLogChannel()

                @dataclass
                class OptionView:
                    embed_desc: str = "Was möchtest du mit **%s** machen?"
                    embed_title: str = "Setup Option"
                    option_name_tickets: str = "Tickets Kategorie"
                    option_name_transcript: str = "Transcript Kategorie"
                    option_name_logchannel: str = "Log Channel"
                    option_name_timeout_logchannel: str = "Timeout Log Channel"
                    option_name_modroles: str = "Moderator Rollen"
                    option_name_language: str = "Server Sprache"
                option_view = OptionView()

                @dataclass
                class SelectView:
                    embed_desc: str = "Wähle eine Setup-Option aus dem Dropdown-Menü:"
                    embed_title: str = "Bot Setup"
                select_view = SelectView()

            @dataclass
            class Language:
                set_success: str = "Die Sprache wurde auf %s gesetzt."
                current: str = "Die aktuelle Sprache ist %s."
                unknown: str = "Fehler: Unbekannte Sprache"
            language = Language()
            button = Button()
        setup = Setup()

        @dataclass
        class Category:
            @dataclass
            class Create:
                success_desc: str = "Kategorie '%s' erfolgreich erstellt!"
                success_title: str = "Kategorie erstellt"
                field_id: str = "ID"
                field_name: str = "Name"
                field_emoji: str = "Emoji"
                field_description: str = "Beschreibung"

                @dataclass
                class Modal:
                    title: str = "Neue Kategorie erstellen"
                    name_label: str = "Name"
                    name_placeholder: str = "z.B. Support, Bewerbung, Bug Report"
                    emoji_label: str = "Emoji"
                    emoji_placeholder: str = "z.B. 🎫, 📝, 🐛 (Unicode oder Discord Emoji)"
                    description_label: str = "Beschreibung"
                    description_placeholder: str = "Kurze Beschreibung der Kategorie"
                modal = Modal()
            create = Create()

            @dataclass
            class Edit:
                not_found: str = "Kategorie nicht gefunden!"
                no_categories_found_desc: str = "Keine Kategorien gefunden. Verwende '/category create' um eine zu erstellen."
                no_categories_found_title: str = "Keine Kategorien"
                select_prompt: str = "Wähle eine Kategorie zum Bearbeiten:"
                select_title: str = "Kategorie bearbeiten"
                update_success_desc: str = "Kategorie '%s' erfolgreich aktualisiert!"
                update_success_title: str = "Kategorie aktualisiert"

                @dataclass
                class Modal:
                    title: str = "Bearbeite %s"
                    name_label: str = "Name"
                    name_placeholder: str = "Name der Kategorie"
                    emoji_label: str = "Emoji"
                    emoji_placeholder: str = "Emoji für die Kategorie"
                    description_label: str = "Beschreibung"
                    description_placeholder: str = "Beschreibung der Kategorie"
                modal = Modal()

                @dataclass
                class Select:
                    placeholder: str = "Kategorie zum Bearbeiten wählen..."
                select = Select()

                @dataclass
                class Options:
                    description: str = "Bearbeite Kategorie: %s %s"
                    title: str = "Kategorie bearbeiten"
                    button_basic_info: str = "Name/Emoji/Beschreibung"
                    button_roles: str = "Rollen-Berechtigung"
                    button_questions: str = "Fragen"
                options = Options()

                @dataclass
                class Roles:
                    description: str = "Berechtigungen für: %s %s"
                    title: str = "Rollen-Berechtigung bearbeiten"
                    current_roles_field: str = "Aktuelle Rollen"
                    current_permission_field: str = "Aktuelle Berechtigung"
                    all_users_permission: str = "Alle Benutzer können diese Kategorie verwenden"
                roles = Roles()

                @dataclass
                class Questions:
                    description: str = "Fragen für: %s %s"
                    title: str = "Fragen bearbeiten"
                    current_questions_field: str = "Aktuelle Fragen"
                    questions_field: str = "Fragen"
                    no_questions: str = "Keine Fragen konfiguriert"
                questions = Questions()
            edit = Edit()

            @dataclass
            class Menu:
                description: str = "Wähle eine Aktion für die Kategorie-Verwaltung:"
                title: str = "📂 Kategorie-Verwaltung"
                button_label: str = "Kategorien verwalten"
            menu = Menu()

            @dataclass
            class Questions:
                @dataclass
                class Modal:
                    title: str = "Fragen: %s"
                    question_label: str = "Frage %d"
                    no_answers: str = "Keine Antworten erhalten."
                    unknown_question: str = "Unbekannte Frage"
                modal = Modal()

                @dataclass
                class AddModal:
                    title: str = "Frage hinzufügen: %s"
                    question_label: str = "Frage"
                    question_placeholder: str = "Gib deine Frage ein..."
                add_modal = AddModal()

                @dataclass
                class ReplaceModal:
                    title: str = "Fragen ersetzen: %s"
                    questions_label: str = "Fragen (eine pro Zeile)"
                    questions_placeholder: str = "Frage 1\nFrage 2\nFrage 3\n..."
                replace_modal = ReplaceModal()

                @dataclass
                class EditView:
                    add_success_desc: str = "Frage zu '%s' hinzugefügt: %s"
                    add_success_title: str = "Frage hinzugefügt"
                    replace_success_desc: str = "Fragen für '%s' aktualisiert (%d Fragen)"
                    replace_success_title: str = "Fragen aktualisiert"
                    clear_success_desc: str = "Alle Fragen für '%s' wurden gelöscht"
                    clear_success_title: str = "Fragen gelöscht"
                edit_view = EditView()
            questions = Questions()

            @dataclass
            class Remove:
                delete_success: str = "Kategorie '%s' wurde erfolgreich gelöscht."
                delete_success_title: str = "Kategorie gelöscht"
                delete_cancelled: str = "Kategorie-Löschung abgebrochen."
                delete_cancelled_title: str = "Abgebrochen"
                not_found: str = "Kategorie nicht gefunden"
                confirm_embed_desc: str = "**Name:** %s\n**Emoji:** %s\n**Beschreibung:** %s\n\n**⚠️ Warnung:** Diese Aktion kann nicht rückgängig gemacht werden!\nAlle Fragen und Rollen-Zuweisungen werden ebenfalls gelöscht."
                no_description: str = "Keine Beschreibung"
                confirm_embed_title: str = "Kategorie '%s' löschen?"
                no_categories_found: str = "Keine Kategorien gefunden. Verwende '/category create' um eine zu erstellen."
                no_categories_found_title: str = "Keine Kategorien"
                select_prompt: str = "Wähle eine Kategorie zum Löschen:"
                select_prompt_title: str = "Kategorie löschen"
                still_active_tickets: str = "Kategorie hat noch %d aktive Tickets."
            remove = Remove()

            @dataclass
            class Roles:
                permissions_limited: str = "Berechtigung für '%s' auf folgende Rollen beschränkt: %s"
                permissions_all_users: str = "Kategorie '%s' ist jetzt für alle Benutzer verfügbar."
                permissions_updated_title: str = "Berechtigung aktualisiert"
            roles = Roles()
        category = Category()

        @dataclass
        class Panel:
            test_category_name: str = "Test Kategorie"
            test_category_description: str = "Dies ist eine Testkategorie"
            no_categories_found: str = "Keine verfügbaren Ticket-Kategorien gefunden."
            no_description: str = "Keine Beschreibung"
            category_not_found: str = "Kategorie nicht gefunden"
            no_permission: str = "Du hast keine Berechtigung, diese Kategorie zu verwenden"
            error_creating_ticket: str = "Fehler beim Erstellen des Tickets: %s"
            default_category_name: str = "ticket"
            answers: str = "Antworten"
            welcome_message: str = "Willkommen %s! %s"
            no_categories_configured_error: str = "Keine Ticket-Kategorien gefunden!\n\nErstelle zuerst Kategorien mit `/category create`, bevor du ein Panel erstellst."
            panel_view_error: str = "Fehler beim Erstellen der Panel-Ansicht: %s"
        panel = Panel()
    feature = Feature()

    @dataclass
    class Command:
        @dataclass
        class Giveaway:
            name: str = "giveaway"
            desc: str = "Starte ein Giveaway mit automatischer Gewinnermittlung."

            @dataclass
            class Option:
                duration: str = "dauer"
                winner_count: str = "gewinner"
                role: str = "rolle"
                prize: str = "preis"
                duration_desc: str = "Dauer des Giveaways"
                winner_count_desc: str = "Anzahl der Gewinner"
                role_desc: str = "Rolle, die die Gewinner erhalten (optional)"
                prize_desc: str = "Preis des Giveaways"
            option = Option()
        giveaway = Giveaway()

        @dataclass
        class Team:
            name: str = "team"
            desc: str = "Verwaltet Team-Mitglieder und Listen."

            @dataclass
            class Add:
                name: str = "add"
                desc: str = "Fügt einen Benutzer zu einem Team hinzu und weist eine Rolle zu."

                @dataclass
                class Option:
                    user: str = "user"
                    role: str = "role"
                    user_desc: str = "Der Benutzer, der zum Team hinzugefügt werden soll."
                    role_desc: str = "Die Rolle, die dem Benutzer zugewiesen werden soll."
                option = Option()
            add = Add()

            @dataclass
            class Remove:
                name: str = "remove"
                desc: str = "Entfernt eine Rolle von einem Benutzer."

                @dataclass
                class Option:
                    user: str = "user"
                    role: str = "role"
                    user_desc: str = "Der Benutzer, von dem die Rolle entfernt werden soll."
                    role_desc: str = "Die Rolle, die entfernt werden soll."
                option = Option()
            remove = Remove()

            @dataclass
            class Wechsel:
                name: str = "wechsel"
                desc: str = "Wechselt die Rolle eines Benutzers."

                @dataclass
                class Option:
                    user: str = "user"
                    from_role: str = "von"
                    to_role: str = "zu"
                    user_desc: str = "Der Benutzer, dessen Rolle gewechselt werden soll."
                    from_role_desc: str = "Die Rolle, die entfernt werden soll."
                    to_role_desc: str = "Die Rolle, die hinzugefügt werden soll."
                option = Option()
            wechsel = Wechsel()

            @dataclass
            class List:
                name: str = "list"
                desc: str = "Listet Team-Mitglieder basierend auf ausgewählten Rollen auf."
            list = List()

            @dataclass
            class Sperre:
                name: str = "sperre"
                desc: str = "Sperrt einen Benutzer für die Ticketerstellung (Bewerbungen)."

                @dataclass
                class Option:
                    user: str = "user"
                    duration: str = "duration"
                    user_desc: str = "Der zu sperrende Benutzer."
                    duration_desc: str = "Dauer der Sperre (z.B. 7d, 4w, permanent)."
                option = Option()
            sperre = Sperre()

            @dataclass
            class Welcome:
                name: str = "welcome"
                desc: str = "Zeigt/Setzt den Willkommens-Channel."

                @dataclass
                class Option:
                    channel: str = "channel"
                    channel_desc: str = "Der Channel, in dem neue Team-Mitglieder begrüßt werden sollen."
                option = Option()
            welcome = Welcome()
        team = Team()

        @dataclass
        class Timeout:
            name: str = "timeout"
            desc: str = "Timeoutet einen Benutzer für eine bestimmte Dauer."

            @dataclass
            class Option:
                user: str = "user"
                duration: str = "duration"
                reason: str = "reason"
                user_desc: str = "Der Benutzer, der getimeoutet werden soll."
                duration_desc: str = "Dauer des Timeouts (z.B. 1m, 2h, 3d)."
                reason_desc: str = "Grund für den Timeout (optional)."
            option = Option()
        timeout = Timeout()

        @dataclass
        class Ticket:
            name: str = "ticket"
            desc: str = "Öffne das Ticket-Menü mit verschiedenen Optionen."
        ticket = Ticket()

        @dataclass
        class Setup:
            name: str = "setup"
            desc: str = "Konfiguriert den Bot."

            @dataclass
            class Tickets:
                name: str = "tickets"
                desc: str = "Die Kategorie, in der Tickets erstellt werden sollen."

                @dataclass
                class Option:
                    category: str = "category"
                    category_desc: str = "Die Kategorie für neue Tickets."
                option = Option()
            tickets = Tickets()

            @dataclass
            class Transcript:
                name: str = "transcript"
                desc: str = "Die Kategorie, in der Transkripte/alte Tickets gespeichert werden sollen."

                @dataclass
                class Option:
                    category: str = "category"
                    category_desc: str = "Die Kategorie für Transkripte."
                option = Option()
            transcript = Transcript()

            @dataclass
            class Logchannel:
                name: str = "logchannel"
                desc: str = "Konfiguriert den Log-Channel für Team-Aktionen."

                @dataclass
                class Option:
                    channel: str = "channel"
                    channel_desc: str = "Der Log-Channel für Team-Aktionen."
                option = Option()
            logchannel = Logchannel()

            @dataclass
            class Timeoutlogchannel:
                name: str = "timeoutlogchannel"
                desc: str = "Konfiguriert den Log-Channel für Timeouts."

                @dataclass
                class Option:
                    channel: str = "channel"
                    channel_desc: str = "Der Log-Channel für Timeouts."
                option = Option()
            timeoutlogchannel = Timeoutlogchannel()

            @dataclass
            class Modroles:
                name: str = "modroles"
                desc: str = "Konfiguriert die Moderator-Rollen (mehrere auswählbar)."
            modroles = Modroles()

            @dataclass
            class Language:
                name: str = "sprache"
                desc: str = "Ändert die Sprache des Bots für diesen Server."

                @dataclass
                class Option:
                    language: str = "sprache"
                    language_desc: str = "Die zu verwendende Sprache."
                option = Option()
            language = Language()
        setup = Setup()

        @dataclass
        class Ping:
            name: str = "ping"
            desc: str = "Testet ob der Bot antwortet."
        ping = Ping()

        @dataclass
        class Createpanel:
            name: str = "createpanel"
            desc: str = "Erstelle eine Nachricht mit einem Knopf um ein Ticket zu erstellen."
        createpanel = Createpanel()

        @dataclass
        class Help:
            name: str = "help"
            desc: str = "Zeigt alle verfügbaren Bot-Befehle an."
        help = Help()

        @dataclass
        class Category:
            name: str = "category"
            desc: str = "Verwalte benutzerdefinierte Ticket-Kategorien"

            @dataclass
            class Create:
                name: str = "create"
                desc: str = "Erstelle eine neue Ticket-Kategorie"
            create = Create()

            @dataclass
            class Edit:
                name: str = "edit"
                desc: str = "Bearbeite eine existierende Ticket-Kategorie"
            edit = Edit()

            @dataclass
            class Remove:
                name: str = "remove"
                desc: str = "Entferne eine Ticket-Kategorie"
            remove = Remove()
        category = Category()

        @dataclass
        class Banlist:
            name: str = "banlist"
            desc: str = "Verwaltet die Banliste."

            @dataclass
            class Show:
                name: str = "show"
                desc: str = "Zeigt die aktuelle Banliste an."
            show = Show()

            @dataclass
            class Add:
                name: str = "add"
                desc: str = "Fügt einen Benutzer zur Banliste hinzu."

                @dataclass
                class Option:
                    name: str = "name"
                    reason: str = "reason"
                    banned_by: str = "banned_by"
                    length: str = "length"
                    image_url: str = "image_url"
                    name_desc: str = "Der Name des zu bannenden Benutzers."
                    reason_desc: str = "Der Grund für den Bann."
                    banned_by_desc: str = "Wer hat den Benutzer gebannt."
                    length_desc: str = "Die Dauer des Banns."
                    image_desc: str = "URL zu einem Bild (optional)"
                option = Option()
            add = Add()

            @dataclass
            class Remove:
                name: str = "remove"
                desc: str = "Entfernt einen Benutzer von der Banliste."

                @dataclass
                class Option:
                    name: str = "name"
                    name_desc: str = "Der Name des zu entbannenden Benutzers."
                option = Option()
            remove = Remove()

            @dataclass
            class Showimg:
                name: str = "showimg"
                desc: str = "Zeigt das Bild eines gebannten Benutzers an."

                @dataclass
                class Option:
                    name: str = "name"
                    name_desc: str = "Der Name des gebannten Benutzers."
                option = Option()
            showimg = Showimg()
        banlist = Banlist()
    command = Command()

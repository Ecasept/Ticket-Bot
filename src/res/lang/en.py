from dataclasses import dataclass

from src.constants import C


@dataclass
class ResEN:
    """
    English string resources for the bot's UI and messages.
    """
    bot_activity: str = "on /help"

    error_title: str = "Error"
    error_occurred: str = "An error occurred: %s"

    user_id_invalid: str = "The user ID is invalid."
    user_not_found: str = "The user <@%s> could not be found on the server."

    panel_msg: str = "Select a category to create a ticket."
    create_ticket_button: str = "Create Ticket"
    ticket_msg_created: str = "Users can use the button below to create tickets!"
    ticket_panel_title: str = "Ticket Support"

    application_emoji: str = "📝"
    support_emoji: str = "🛠️"
    report_emoji: str = "🚨"

    delete_emoji: str = "⛔"
    reopen_emoji: str = "🔄"

    close_emoji: str = "🔒"  # not an x because the bg of the button is red
    mod_options_emoji: str = "⚙️"

    invalid_duration: str = "❌ Invalid duration `%s`. Use e.g. `10s`, `1m`, `2h`."

    ticket_channel_created: str = "Ticket created! %s"
    ticket: str = "ticket"

    ping_response: str = "Pong!"

    # Ticket menu
    ticket_menu_title: str = "Ticket Menu"
    ticket_menu_description: str = "Select an option from the available ticket commands:"
    ticket_menu_giveaway: str = "Giveaway"
    ticket_menu_timeout: str = "Timeout"
    ticket_menu_setup: str = "Setup"
    ticket_menu_giveaway_desc: str = "Start a giveaway"
    ticket_menu_timeout_desc: str = "Timeout a user"
    ticket_menu_setup_desc: str = "Configure bot settings"

    # Setup button labels
    setup_set_value: str = "Set Value"
    setup_view_value: str = "View Value"

    close_ticket: str = "Close"
    ticket_closed_msg: str = "The ticket was closed by %s."

    ticket_category_title: str = "Create a Ticket"
    ticket_category_placeholder: str = "Select a category"
    ticket_category_select_placeholder: str = "Select a ticket category..."

    application: str = "Application"
    report: str = "Report"
    support: str = "Support"
    application_prefix: str = "application"
    report_prefix: str = "report"
    support_prefix: str = "support"
    application_desc: str = "Submit a new application"
    report_desc: str = "Report a user"
    support_desc: str = "Help with general questions"

    choose_category: str = "Choose a category for your ticket."

    assign_ticket: str = "Assign"
    assign_emoji: str = "📥"
    unassign_ticket: str = "Unassign"
    unassign_emoji: str = "📤"

    mod_options_title: str = "Mod Options"
    mod_options_no_permission: str = "You do not have permission to use these options."
    mod_options_user: str = "Creator"
    mod_options_assignee: str = "Assigned to"
    mod_options_unassigned: str = "Unassigned"
    mod_options_category: str = "Category"
    mod_options_created_at: str = "Created at"
    mod_options_archived: str = "Archived"
    mod_options_archived_yes: str = "Yes"
    mod_options_archived_no: str = "No"
    noch_fragen_label: str = "Any questions?"
    noch_fragen_emoji: str = "❓"

    approve_application: str = "Approve Application"
    approve_application_emoji: str = "✅"
    reject_application: str = "Reject Application"
    reject_application_emoji: str = "⛔"

    # Application rejection modal
    reject_application_modal_title: str = "Reject Application"
    reject_application_reason_label: str = "Reason for rejection"
    reject_application_reason_placeholder: str = "Provide a reason (optional)"
    application_rejected_with_reason_msg: str = "%s, your application was rejected for the following reason: %s"
    application_rejected_msg: str = "%s, your application has been rejected."

    close_ticket_request_title: str = "Close ticket?"

    header_msg_application: str = "Welcome to the ticket, %s! Here you can submit your application"
    header_msg_report: str = "Welcome to the ticket, %s! Here you can report someone"
    header_msg_support: str = "Welcome to the ticket, %s! Here you can ask for support"
    header_title_support: str = "Ticket Support"
    header_title_application: str = "Application"
    header_title_report: str = "Report"
    header_footer: str = "Ticket ID: %s"

    ticket_not_found_msg: str = "Ticket not found. Please create a new ticket."

    application_approved_msg: str = "Congratulations, %s! Your application has been approved."
    application_rejected_msg: str = "Unfortunately, your application has been rejected, %s."

    continue_button: str = "Continue"

    ticket_not_found: str = "This ticket could not be found in the database."
    ticket_already_closed: str = "This ticket is already closed."
    ticket_close_no_permission: str = "You do not have permission to close this ticket."

    ticket_close_request_msg: str = "%s wants to close this ticket."
    ticket_close_request_accept: str = "Accept"
    ticket_close_request_decline: str = "Decline"
    ticket_close_request_declined_msg: str = "%s, your request to close the ticket has been declined."
    ticket_close_request_decline_no_permission: str = "You do not have permission to decline this request."
    ticket_close_request_accept_no_permission: str = "You do not have permission to accept this request."

    delete_ticket_button: str = "Delete"
    reopen_ticket_button: str = "Reopen"
    ticket_delete_no_permission: str = "You do not have permission to delete this ticket."
    ticket_reopen_no_permission: str = "You do not have permission to reopen this ticket."
    ticket_reopened_msg: str = "The ticket was reopened by %s."

    ticket_assigned_msg: str = "The ticket has been assigned to %s."
    ticket_unassigned_msg: str = "The ticket has been unassigned."

    # Giveaway strings
    giveaway_desc: str = "Start a giveaway with automatic winner selection."
    giveaway_duration_desc: str = "Duration of the giveaway (e.g. 30s, 2m, 1h)"
    giveaway_prize_desc: str = "What is the prize?"
    giveaway_winners_desc: str = "Number of winners"
    giveaway_role_desc: str = "Role that winners will receive (optional)"

    giveaway_duration_extreme: str = "❌ Duration must be between 10 seconds and 30 days."
    giveaway_invalid_winners: str = "❌ Invalid number of winners. Must be between 1 and 20."
    giveaway_started: str = "✅ Giveaway has been started!"
    giveaway_title: str = "🎉 Giveaway: %s"
    giveaway_description: str = "**%s** is being given away!\n🏆 **%s** winners will be selected"
    giveaway_ends_at: str = "🕐 Ends at"
    giveaway_role_prize: str = "🎭 Additional Role"
    giveaway_participation: str = "📝 Participation"
    giveaway_react_to_participate: str = "React with %s to participate!"
    giveaway_footer: str = "Hosted by User ID: %s"
    giveaway_prize: str = "**Prize:** %s"
    giveaway_duration: str = "**Duration:** %s"
    giveaway_role: str = "**Role:** %s"
    giveaway_host: str = "Hosted by: %s"
    giveaway_winner_count: str = "Winners: %s"

    giveaway_winners_announcement: str = "🎊 Congratulations %s! You have won **%s**!"
    giveaway_no_participants: str = "Nobody won the giveaway because nobody participated."
    giveaway_ended_title: str = "🎉 Giveaway ended"
    giveaway_role_awarded: str = "✅ Role %s has been awarded to the winners."
    giveaway_role_perms_error: str = "⚠️ Could not award %s to %s (missing permissions)."
    giveaway_not_found: str = "Giveaway not found in the database."
    giveaway_already_ended: str = "This giveaway has already ended."
    giveaway_no_role: str = "No role"

    # setup.py
    setup_title: str = "Setup"
    setup_no_ticket_category = "There is currently no category set for tickets."
    setup_tickets_current_category = "The current ticket category is %s."
    setup_tickets_set_category = "The ticket category has been set to %s."
    setup_ticket_category_not_found = "The category for tickets could not be found. Please make sure the category exists and the bot has permission to see it."

    # setup_transcript
    setup_no_transcript_category = "There is currently no category set for transcripts."
    setup_transcript_current_category = "The current transcript category is %s."
    setup_transcript_set_category = "The transcript category has been set to %s."
    setup_transcript_category_not_found = "The category for transcripts could not be found. Please make sure the category exists and the bot has permission to see it."

    # Setup Log Channel
    setup_no_logchannel: str = "No log channel for team actions is configured."
    setup_logchannel_not_found: str = "The configured log channel was not found on this server. Please make sure the channel exists and the bot has permission to see it."
    setup_logchannel_current: str = "The current log channel for team actions is %s."
    setup_logchannel_set: str = "The log channel for team actions has been set to %s."
    log_channel_title: str = "Team Log Channel"

    # Setup Mod Roles (multiple)
    setup_modroles_select_prompt: str = "Please select the moderator roles."
    setup_modroles_select_placeholder: str = "Select moderator roles"
    setup_modroles_set: str = "The moderator roles have been set to %s."
    setup_modroles_none_selected: str = "Please select at least one role."
    setup_modroles_current: str = "The current moderator roles are: %s."
    mod_roles_title: str = "Moderator Roles"
    setup_no_modroles: str = "No moderator roles are configured."
    setup_modroles_not_found: str = "One or more configured moderator roles could not be found on the server. Please make sure the roles exist and the bot has permission to see them."
    modroles_submit_button_label: str = "Select"
    setup_modroles_invalid: str = "One or more selected mod roles are invalid. Please select valid roles."

    # Team Commands
    team_add_success_log: str = "%s was assigned the role %s by %s."
    team_add_no_log_channel: str = "Error: Please configure a log channel first with `/setup logchannel`."
    team_list_select_roles_prompt: str = "Please select the roles to be displayed as team roles."
    team_list_role_select_placeholder: str = "Select roles"
    team_list_submit_button_label: str = "Display"
    team_list_embed_title: str = "Team Members"
    team_list_no_members_found: str = "No members found with this role."
    team_list_update_button_label: str = "Update"
    team_list_upate_emoji: str = "🔄"
    team_list_select_at_least_one_role: str = "Please select at least one role."
    team_list_old_version: str = "This team list was created with an older version of the bot. Please delete it and create a new one."
    status_online: str = "🟢"
    status_idle: str = "🟡"
    status_dnd: str = "⛔"
    status_offline: str = "⚫"
    status_unknown: str = "❓"
    status_mobile: str = "📱"
    add_role_no_perm: str = "The bot does not have permission to access this role."
    new_team_member_title: str = "New Team Member"

    team_remove_success_log: str = "%s was removed from the role %s by %s."
    team_remove_no_log_channel: str = "Error: Please configure a log channel first with `/setup logchannel`."
    team_remove_success_title: str = "Team Member Removed"
    team_remove_user_missing_role: str = "The user does not have this role."

    team_welcome_no_channel: str = "No welcome channel is configured."
    team_welcome_current_channel: str = "The current welcome channel is %s."
    team_welcome_channel_set: str = "The welcome channel has been set to %s."
    team_welcome_channel_not_found: str = "The welcome channel could not be found."
    welcome_message: str = "Welcome %s, you are now %s."

    team_wechsel_success_log: str = "%s was switched from %s to %s by %s."
    team_wechsel_success_title: str = "Team Role Switched"
    team_wechsel_user_missing_from_role: str = "The user does not have the old role."
    team_wechsel_user_already_has_to_role: str = "The user already has the new role."

    # Application
    application_cancelled: str = "The application has been cancelled."
    application_info: str = "Please enter the information for your application."
    application_age_label: str = "Age"
    application_age_placeholder: str = "Enter your age"
    application_apply_for_label: str = "What do you want to apply for?"
    application_apply_for_placeholder: str = "E.g. Moderator, Developer"
    application_text_label: str = "Application Text"
    application_text_placeholder: str = "Write your application here..."

    # Noch Fragen functionality
    noch_fragen_msg: str = "Do you have any more questions? If not, this ticket will be closed automatically in %d hours."
    noch_fragen_title: str = "Ticket will be closed"
    no_questions: str = "No more questions"
    noch_fragen_delete_emoji: str = "✅"
    no_questions_cancel: str = "I still have questions"
    noch_fragen_cancel_emoji: str = "❓"
    noch_fragen_no_permission: str = "Only the creator can answer the questions."
    ticket_noch_fragen_close_error_title: str = "Error during automatic closing"
    ticket_no_close_time: str = "This ticket is not (anymore) configured for automatic closing. Please close it manually."
    noch_fragen_cancel_msg: str = "%s, you can now ask questions again."
    noch_fragen_delete_msg: str = "The ticket will now be deleted. The channel will no longer be usable."
    noch_fragen_closed_msg: str = "The ticket was closed automatically."

    # Help command
    help_desc: str = "Shows all available bot commands."
    help_title: str = "🤖 Bot Help"
    help_description: str = "Here are all available commands for this bot:"
    help_general_commands: str = "📋 **General Commands**"
    help_setup_commands: str = "⚙️ **Setup Commands** (Administrator required)"
    help_team_commands: str = "👥 **Team Commands** (Administrator required)"
    help_tutorial_title: str = "🚀 **First Steps**"
    help_tutorial_text: str = f"**Setup Order:**\n1️⃣ `/setup tickets` - Set category for new tickets\n2️⃣ `/setup transcript` - Set category for closed tickets\n3️⃣ `/setup modroles` - Select moderator roles\n4️⃣ `/setup logchannel` - Log channel for team actions *(optional)*\n5️⃣ `/createpanel` - Create ticket panel for users\n\n✨ **Tip:** Your question was not answered? Create a ticket on our [Support Server]({C.support_guild_invite_link})!"
    help_footer: str = f"{C.bot_name} - Tickets & more"

    # Timeout
    timeout_success: str = "✅ %s has been timed out for %s. Reason: %s"
    timeout_success_no_reason: str = "✅ %s has been timed out for %s."
    timeout_dm_notification: str = "You have been timed out on the server '%s' for %s. Reason: %s"
    timeout_dm_notification_no_reason: str = "You have been timed out on the server '%s' for %s."
    timeout_log_title: str = "📛 Timeout"
    timeout_log_user: str = "👤 User"
    timeout_log_duration: str = "⏱ Duration"
    timeout_log_reason: str = "📝 Reason"
    timeout_log_moderator: str = "👮 By"
    timeout_log_no_reason: str = "No reason provided"
    timeout_invalid_duration: str = "❌ Invalid duration. Use e.g. `1m`, `2h`, `3d`."
    timeout_duration_too_long: str = "❌ Timeout duration can be at most 28 days."
    timeout_cant_timeout_self: str = "❌ You can't timeout yourself."
    timeout_cant_timeout_bot: str = "❌ You can't timeout the bot."
    timeout_failed: str = "❌ Timeout failed: %s"
    setup_timeout_logchannel_desc: str = "Configures the log channel for timeouts."
    setup_no_timeout_logchannel: str = "No log channel for timeouts is configured."
    setup_timeout_logchannel_not_found: str = "The configured timeout log channel was not found on this server."
    setup_timeout_logchannel_current: str = "The current timeout log channel is %s."
    setup_timeout_logchannel_set: str = "The timeout log channel has been set to %s."
    timeout_log_channel_title: str = "Timeout Log Channel"

    # Application Ban
    team_sperre_desc: str = "Bans a user from creating application tickets."
    team_sperre_user_desc: str = "The user to be banned."
    team_sperre_duration_desc: str = "Duration of the ban (e.g. 1d, 2w, 3m). Optional, default is forever."
    team_sperre_success: str = "✅ %s has been banned from creating application tickets."
    team_sperre_already_banned: str = "❌ %s is already banned from creating application tickets."

    team_sperre_unban: str = "Lift ban"
    team_sperre_unban_emoji: str = "🔓"
    team_sperre_unban_success: str = "✅ %s has been unbanned from creating application tickets."

    application_banned_message: str = "❌ You are banned from creating application tickets and cannot submit new applications."

    team_sperre_logging_failed_suffix: str = "\nThe user was banned anyway."
    team_sperre_success_log_duration: str = "%s was banned by %s for `%s` from creating application tickets."
    team_sperre_success_log: str = "%s was banned by %s from creating application tickets."
    team_sperre_success_title: str = "Application Ban"
    team_sperre_unban_log: str = "%s has lifted the ban of %s for application tickets."
    team_sperre_unban_log_title: str = "Application Ban Lifted"

    # Banlist
    banlist_group_desc: str = "Manages the ban list."
    banlist_show_desc: str = "Shows the current ban list."
    banlist_add_desc: str = "Adds a user to the ban list."
    banlist_remove_desc: str = "Removes a user from the ban list."
    banlist_add_name_desc: str = "The name of the user to be banned."
    banlist_add_reason_desc: str = "The reason for the ban."
    banlist_add_banned_by_desc: str = "Who banned the user."
    banlist_add_length_desc: str = "The duration of the ban."
    banlist_remove_name_desc: str = "The name of the user to be unbanned."
    banlist_embed_title: str = "Ban List"
    banlist_no_bans: str = "The ban list is empty."
    banlist_add_success: str = "✅ %s has been added to the ban list."
    banlist_add_failed: str = "❌ Could not add %s to the ban list: %s"
    banlist_remove_success: str = "✅ %s has been removed from the ban list."
    banlist_remove_failed: str = "❌ Could not remove %s from the ban list: %s"
    banlist_already_banned: str = "❌ %s is already on the ban list."
    banlist_not_banned: str = "❌ %s is not on the ban list."
    banlist_item_banned_by_for: str = "Banned by **%s** for **%s**"
    banlist_item_reason: str = "Reason: %s"
    list_too_long: str = "The list is too long to be displayed in an embed."
    update_button_label: str = "Update"

    banlist_no_image: str = "❌ %s has no image."
    banlist_image_indicator: str = " + Image"
    banlist_invalid_url: str = "❌ The provided URL is invalid. Please provide a valid HTTP/HTTPS URL."
    banlist_showimg_embed_title = "Image of %s"

    # Category management strings
    category_new: str = "New Category"
    category_edit: str = "Edit Category"
    category_delete: str = "Delete Category"
    category_yes_delete: str = "Yes, delete"
    category_cancel: str = "Cancel"
    category_save: str = "Save"
    category_name_label: str = "Name"
    category_name_placeholder: str = "Name of the category"
    category_emoji_label: str = "Emoji"
    category_emoji_placeholder: str = "Emoji for the category"
    category_description_label: str = "Description"
    category_description_placeholder: str = "Description of the category"
    category_name_emoji_desc: str = "Name/Emoji/Description"
    category_roles_permission: str = "Role Permission"
    category_questions: str = "Questions"
    category_questions_count: str = "Questions (%d)"
    category_select_label: str = "Categories"
    category_select_placeholder: str = "Select a category to delete..."
    category_roles_placeholder: str = "Select roles (empty = all users)..."
    category_field_id: str = "ID"
    category_field_permission: str = "Permission"
    category_field_all_users: str = "All users"
    category_field_no_questions: str = "No questions configured"
    category_field_no_description: str = "No description"

    # Category creation
    category_create_name_placeholder: str = "e.g. Support, Application, Bug Report"
    category_create_emoji_placeholder: str = "e.g. 🎫, 📝, 🐛 (Unicode or Discord Emoji)"
    category_create_description_placeholder: str = "Short description of the category"

    # Category questions
    category_question_label: str = "Question"
    category_questions_all_label: str = "Questions (one per line)"
    category_question_add: str = "Add Question"
    category_questions_replace_all: str = "Replace All Questions"
    category_questions_delete_all: str = "Delete All Questions"

    # Timeout interface strings
    timeout_user_select_placeholder: str = "Select a user to timeout"
    timeout_duration_select_placeholder: str = "Select a timeout duration"
    timeout_execute_button: str = "Execute Timeout"
    timeout_cancel_button: str = "Cancel"
    timeout_30s_label: str = "30 seconds"
    timeout_30s_desc: str = "Short timeout"
    timeout_5m_label: str = "5 minutes"
    timeout_5m_desc: str = "Standard timeout"
    timeout_1h_label: str = "1 hour"
    timeout_1h_desc: str = "Longer timeout"
    timeout_1d_label: str = "1 day"
    timeout_1d_desc: str = "Daily timeout"
    timeout_1w_label: str = "1 week"
    timeout_1w_desc: str = "Weekly timeout"
    timeout_select_user_error: str = "❌ Please select a user."
    timeout_select_duration_error: str = "❌ Please select a timeout duration."
    timeout_user_not_on_server: str = "❌ User is not on this server."
    timeout_cancelled: str = "Timeout cancelled."
    timeout_interface_title: str = "User Timeout"
    timeout_interface_description: str = "Select a user and a timeout duration from the dropdown menus:"

    # Giveaway interface strings
    giveaway_duration_select_placeholder: str = "Select a giveaway duration"
    giveaway_duration_30s_label: str = "30 seconds"
    giveaway_duration_30s_desc: str = "Test giveaway"
    giveaway_duration_5m_label: str = "5 minutes"
    giveaway_duration_5m_desc: str = "Short giveaway"
    giveaway_duration_1h_label: str = "1 hour"
    giveaway_duration_1h_desc: str = "Standard giveaway"
    giveaway_duration_1d_label: str = "1 day"
    giveaway_duration_1d_desc: str = "Daily giveaway"
    giveaway_duration_1w_label: str = "1 week"
    giveaway_duration_1w_desc: str = "Weekly giveaway"

    giveaway_winner_count_select_placeholder: str = "Select number of winners"
    giveaway_winner_1_label: str = "1 winner"
    giveaway_winner_2_label: str = "2 winners"
    giveaway_winner_3_label: str = "3 winners"
    giveaway_winner_5_label: str = "5 winners"
    giveaway_winner_10_label: str = "10 winners"

    giveaway_role_select_placeholder: str = "Select a role as a prize (optional)"
    giveaway_set_prize_button: str = "Enter Prize"
    giveaway_start_button: str = "Start Giveaway"
    giveaway_cancel_button: str = "Cancel"

    # Setup placeholders for selects
    setup_tickets_select_placeholder: str = "Select a category for tickets"
    setup_transcript_select_placeholder: str = "Select a category for transcripts"
    setup_logchannel_select_placeholder: str = "Select a log channel"
    setup_timeout_logchannel_select_placeholder: str = "Select a timeout log channel"
    setup_select_option_placeholder: str = "Select a setup option"

    # Setup select option labels and descriptions
    setup_option_tickets_label: str = "Tickets Category"
    setup_option_tickets_desc: str = "Set/view category for tickets"
    setup_option_transcript_label: str = "Transcript Category"
    setup_option_transcript_desc: str = "Set/view category for transcripts"
    setup_option_logchannel_label: str = "Log Channel"
    setup_option_logchannel_desc: str = "Set/view log channel"
    setup_option_timeout_logchannel_label: str = "Timeout Log Channel"
    setup_option_timeout_logchannel_desc: str = "Set/view timeout log channel"
    setup_option_modroles_label: str = "Moderator Roles"
    setup_option_modroles_desc: str = "Set/view moderator roles"

    banlist_showimg_embed_title = "Image of %s"

    # Category select default placeholder
    category_select_default_placeholder: str = "Select category..."

    @dataclass
    class Feature:
        @dataclass
        class Giveaway:
            role_award_reason: str = "Won in a giveaway"

            @dataclass
            class Button:
                config_embed_desc: str = "Configure your giveaway with the dropdown menus and buttons:"
                config_embed_title: str = "Create Giveaway"
                config_embed_steps_name: str = "📋 Steps"
                config_embed_steps_value: str = "1. Select duration\n2. Select number of winners\n3. Select role as prize (optional)\n4. Enter prize\n5. Start giveaway"
                prize_set_success: str = "✅ Prize set: %s"
                no_duration_error: str = "❌ Please select a giveaway duration."
                no_prize_error: str = "❌ Please enter a prize."
                cancelled_msg: str = "Giveaway cancelled."

                @dataclass
                class PrizeModal:
                    title: str = "Set Giveaway Prize"
                    label: str = "What is the prize?"
                    placeholder: str = "e.g. Discord Nitro, Game Key, etc."
                prize_modal = PrizeModal()
            button = Button()
        giveaway = Giveaway()

        @dataclass
        class Setup:
            @dataclass
            class Button:
                @dataclass
                class SetTickets:
                    embed_desc: str = "Select a category for tickets:"
                    embed_title: str = "Set Tickets Category"
                set_tickets = SetTickets()

                @dataclass
                class SetTranscript:
                    embed_desc: str = "Select a category for transcripts:"
                    embed_title: str = "Set Transcript Category"
                set_transcript = SetTranscript()

                @dataclass
                class SetLogChannel:
                    embed_desc: str = "Select a log channel:"
                    embed_title: str = "Set Log Channel"
                set_logchannel = SetLogChannel()

                @dataclass
                class SetTimeoutLogChannel:
                    embed_desc: str = "Select a timeout log channel:"
                    embed_title: str = "Set Timeout Log Channel"
                set_timeout_logchannel = SetTimeoutLogChannel()

                @dataclass
                class OptionView:
                    embed_desc: str = "What do you want to do with **%s**?"
                    embed_title: str = "Setup Option"
                    option_name_tickets: str = "Tickets Category"
                    option_name_transcript: str = "Transcript Category"
                    option_name_logchannel: str = "Log Channel"
                    option_name_timeout_logchannel: str = "Timeout Log Channel"
                    option_name_modroles: str = "Moderator Roles"
                    option_name_language: str = "Server Language"
                option_view = OptionView()

                @dataclass
                class SelectView:
                    embed_desc: str = "Select a setup option from the dropdown menu:"
                    embed_title: str = "Bot Setup"
                select_view = SelectView()

            @dataclass
            class Language:
                set_success: str = "The language has been set to %s."
                current: str = "The current language is %s."
                unknown: str = "Error: Unknown language"
            language = Language()
            button = Button()
        setup = Setup()

        @dataclass
        class Category:
            @dataclass
            class Create:
                success_desc: str = "Category '%s' created successfully!"
                success_title: str = "Category Created"
                field_id: str = "ID"
                field_name: str = "Name"
                field_emoji: str = "Emoji"
                field_description: str = "Description"

                @dataclass
                class Modal:
                    title: str = "Create New Category"
                    name_label: str = "Name"
                    name_placeholder: str = "e.g. Support, Application, Bug Report"
                    emoji_label: str = "Emoji"
                    emoji_placeholder: str = "e.g. 🎫, 📝, 🐛 (Unicode or Discord Emoji)"
                    description_label: str = "Description"
                    description_placeholder: str = "Short description of the category"
                modal = Modal()
            create = Create()

            @dataclass
            class Edit:
                not_found: str = "Category not found!"
                no_categories_found_desc: str = "No categories found. Use '/category create' to create one."
                no_categories_found_title: str = "No Categories"
                select_prompt: str = "Select a category to edit:"
                select_title: str = "Edit Category"
                update_success_desc: str = "Category '%s' updated successfully!"
                update_success_title: str = "Category Updated"

                @dataclass
                class Modal:
                    title: str = "Edit %s"
                    name_label: str = "Name"
                    name_placeholder: str = "Name of the category"
                    emoji_label: str = "Emoji"
                    emoji_placeholder: str = "Emoji for the category"
                    description_label: str = "Description"
                    description_placeholder: str = "Description of the category"
                modal = Modal()

                @dataclass
                class Select:
                    placeholder: str = "Select category to edit..."
                select = Select()

                @dataclass
                class Options:
                    description: str = "Edit category: %s %s"
                    title: str = "Edit Category"
                    button_basic_info: str = "Name/Emoji/Description"
                    button_roles: str = "Role Permission"
                    button_questions: str = "Questions"
                options = Options()

                @dataclass
                class Roles:
                    description: str = "Permissions for: %s %s"
                    title: str = "Edit Role Permission"
                    current_roles_field: str = "Current Roles"
                    current_permission_field: str = "Current Permission"
                    all_users_permission: str = "All users can use this category"
                roles = Roles()

                @dataclass
                class Questions:
                    description: str = "Questions for: %s %s"
                    title: str = "Edit Questions"
                    current_questions_field: str = "Current Questions"
                    questions_field: str = "Questions"
                    no_questions: str = "No questions configured"
                questions = Questions()
            edit = Edit()

            @dataclass
            class Menu:
                description: str = "Select an action for category management:"
                title: str = "📂 Category Management"
                button_label: str = "Manage Categories"
            menu = Menu()

            @dataclass
            class Questions:
                @dataclass
                class Modal:
                    title: str = "Questions: %s"
                    question_label: str = "Question %d"
                    no_answers: str = "No answers received."
                    unknown_question: str = "Unknown question"
                modal = Modal()

                @dataclass
                class AddModal:
                    title: str = "Add Question: %s"
                    question_label: str = "Question"
                    question_placeholder: str = "Enter your question..."
                add_modal = AddModal()

                @dataclass
                class ReplaceModal:
                    title: str = "Replace Questions: %s"
                    questions_label: str = "Questions (one per line)"
                    questions_placeholder: str = "Question 1\nQuestion 2\nQuestion 3\n..."
                replace_modal = ReplaceModal()

                @dataclass
                class EditView:
                    add_success_desc: str = "Question added to '%s': %s"
                    add_success_title: str = "Question Added"
                    replace_success_desc: str = "Questions for '%s' updated (%d questions)"
                    replace_success_title: str = "Questions Updated"
                    clear_success_desc: str = "All questions for '%s' have been deleted"
                    clear_success_title: str = "Questions Deleted"
                edit_view = EditView()
            questions = Questions()

            @dataclass
            class Remove:
                delete_success: str = "Category '%s' has been successfully deleted."
                delete_success_title: str = "Category Deleted"
                delete_cancelled: str = "Category deletion cancelled."
                delete_cancelled_title: str = "Cancelled"
                not_found: str = "Category not found"
                confirm_embed_desc: str = "**Name:** %s\n**Emoji:** %s\n**Description:** %s\n\n**⚠️ Warning:** This action cannot be undone!\nAll questions and role assignments will also be deleted."
                no_description: str = "No description"
                confirm_embed_title: str = "Delete category '%s'?"
                no_categories_found: str = "No categories found. Use '/category create' to create one."
                no_categories_found_title: str = "No Categories"
                select_prompt: str = "Select a category to delete:"
                select_prompt_title: str = "Delete Category"
                still_active_tickets: str = "Category still has %d active tickets."
            remove = Remove()

            @dataclass
            class Roles:
                permissions_limited: str = "Permission for '%s' restricted to the following roles: %s"
                permissions_all_users: str = "Category '%s' is now available to all users."
                permissions_updated_title: str = "Permission Updated"
            roles = Roles()
        category = Category()

        @dataclass
        class Panel:
            test_category_name: str = "Test Category"
            test_category_description: str = "This is a test category"
            no_categories_found: str = "No available ticket categories found."
            no_description: str = "No description"
            category_not_found: str = "Category not found"
            no_permission: str = "You do not have permission to use this category"
            error_creating_ticket: str = "Error creating ticket: %s"
            default_category_name: str = "ticket"
            answers: str = "Answers"
            welcome_message: str = "Welcome %s! %s"
            no_categories_configured_error: str = "No ticket categories found!\n\nPlease create categories with `/category create` before creating a panel."
            panel_view_error: str = "Error creating panel view: %s"
        panel = Panel()
    feature = Feature()

    @dataclass
    class Command:
        @dataclass
        class Giveaway:
            name: str = "giveaway"
            desc: str = "Start a giveaway with automatic winner selection."

            @dataclass
            class Option:
                duration: str = "duration"
                winner_count: str = "winners"
                role: str = "role"
                prize: str = "prize"
                duration_desc: str = "Duration of the giveaway"
                winner_count_desc: str = "Number of winners"
                role_desc: str = "Role that winners will receive (optional)"
                prize_desc: str = "Prize of the giveaway"
            option = Option()
        giveaway = Giveaway()

        @dataclass
        class Team:
            name: str = "team"
            desc: str = "Manages team members and lists."

            @dataclass
            class Add:
                name: str = "add"
                desc: str = "Adds a user to a team and assigns a role."

                @dataclass
                class Option:
                    user: str = "user"
                    role: str = "role"
                    user_desc: str = "The user to be added to the team."
                    role_desc: str = "The role to be assigned to the user."
                option = Option()
            add = Add()

            @dataclass
            class Remove:
                name: str = "remove"
                desc: str = "Removes a role from a user."

                @dataclass
                class Option:
                    user: str = "user"
                    role: str = "role"
                    user_desc: str = "The user from whom the role is to be removed."
                    role_desc: str = "The role to be removed."
                option = Option()
            remove = Remove()

            @dataclass
            class Wechsel:
                name: str = "wechsel"
                desc: str = "Switches the role of a user."

                @dataclass
                class Option:
                    user: str = "user"
                    from_role: str = "from"
                    to_role: str = "to"
                    user_desc: str = "The user whose role is to be switched."
                    from_role_desc: str = "The role to be removed."
                    to_role_desc: str = "The role to be added."
                option = Option()
            wechsel = Wechsel()

            @dataclass
            class List:
                name: str = "list"
                desc: str = "Lists team members based on selected roles."
            list = List()

            @dataclass
            class Sperre:
                name: str = "ban"
                desc: str = "Bans a user from creating application tickets."

                @dataclass
                class Option:
                    user: str = "user"
                    duration: str = "duration"
                    user_desc: str = "The user to be banned."
                    duration_desc: str = "Duration of the ban (e.g. 7d, 4w, permanent)."
                option = Option()
            sperre = Sperre()

            @dataclass
            class Welcome:
                name: str = "welcome"
                desc: str = "Shows/Sets the welcome channel."

                @dataclass
                class Option:
                    channel: str = "channel"
                    channel_desc: str = "The channel where new team members should be welcomed."
                option = Option()
            welcome = Welcome()
        team = Team()

        @dataclass
        class Timeout:
            name: str = "timeout"
            desc: str = "Timeouts a user for a specific duration."

            @dataclass
            class Option:
                user: str = "user"
                duration: str = "duration"
                reason: str = "reason"
                user_desc: str = "The user to be timed out."
                duration_desc: str = "Duration of the timeout (e.g. 1m, 2h, 3d)."
                reason_desc: str = "Reason for the timeout (optional)."
            option = Option()
        timeout = Timeout()

        @dataclass
        class Ticket:
            name: str = "ticket"
            desc: str = "Open the ticket menu with various options."
        ticket = Ticket()

        @dataclass
        class Setup:
            name: str = "setup"
            desc: str = "Configures the bot."

            @dataclass
            class Tickets:
                name: str = "tickets"
                desc: str = "The category in which tickets should be created."

                @dataclass
                class Option:
                    category: str = "category"
                    category_desc: str = "The category for new tickets."
                option = Option()
            tickets = Tickets()

            @dataclass
            class Transcript:
                name: str = "transcript"
                desc: str = "The category in which transcripts/old tickets should be saved."

                @dataclass
                class Option:
                    category: str = "category"
                    category_desc: str = "The category for transcripts."
                option = Option()
            transcript = Transcript()

            @dataclass
            class Logchannel:
                name: str = "logchannel"
                desc: str = "Configures the log channel for team actions."

                @dataclass
                class Option:
                    channel: str = "channel"
                    channel_desc: str = "The log channel for team actions."
                option = Option()
            logchannel = Logchannel()

            @dataclass
            class Timeoutlogchannel:
                name: str = "timeoutlogchannel"
                desc: str = "Configures the log channel for timeouts."

                @dataclass
                class Option:
                    channel: str = "channel"
                    channel_desc: str = "The log channel for timeouts."
                option = Option()
            timeoutlogchannel = Timeoutlogchannel()

            @dataclass
            class Modroles:
                name: str = "modroles"
                desc: str = "Configures the moderator roles (multiple selectable)."
            modroles = Modroles()

            @dataclass
            class Language:
                name: str = "language"
                desc: str = "Changes the bot's language for this server."

                @dataclass
                class Option:
                    language: str = "language"
                    language_desc: str = "The language to be used."
                option = Option()
            language = Language()
        setup = Setup()

        @dataclass
        class Ping:
            name: str = "ping"
            desc: str = "Tests if the bot is responding."
        ping = Ping()

        @dataclass
        class Createpanel:
            name: str = "createpanel"
            desc: str = "Create a message with a button to create a ticket."
        createpanel = Createpanel()

        @dataclass
        class Help:
            name: str = "help"
            desc: str = "Shows all available bot commands."
        help = Help()

        @dataclass
        class Category:
            name: str = "category"
            desc: str = "Manage custom ticket categories"

            @dataclass
            class Create:
                name: str = "create"
                desc: str = "Create a new ticket category"
            create = Create()

            @dataclass
            class Edit:
                name: str = "edit"
                desc: str = "Edit an existing ticket category"
            edit = Edit()

            @dataclass
            class Remove:
                name: str = "remove"
                desc: str = "Remove a ticket category"
            remove = Remove()
        category = Category()

        @dataclass
        class Banlist:
            name: str = "banlist"
            desc: str = "Manages the ban list."

            @dataclass
            class Show:
                name: str = "show"
                desc: str = "Shows the current ban list."
            show = Show()

            @dataclass
            class Add:
                name: str = "add"
                desc: str = "Adds a user to the ban list."

                @dataclass
                class Option:
                    name: str = "name"
                    reason: str = "reason"
                    banned_by: str = "banned_by"
                    length: str = "length"
                    image_url: str = "image_url"
                    name_desc: str = "The name of the user to be banned."
                    reason_desc: str = "The reason for the ban."
                    banned_by_desc: str = "Who banned the user."
                    length_desc: str = "The duration of the ban."
                    image_desc: str = "URL to an image (optional)"
                option = Option()
            add = Add()

            @dataclass
            class Remove:
                name: str = "remove"
                desc: str = "Removes a user from the ban list."

                @dataclass
                class Option:
                    name: str = "name"
                    name_desc: str = "The name of the user to be unbanned."
                option = Option()
            remove = Remove()

            @dataclass
            class Showimg:
                name: str = "showimg"
                desc: str = "Shows the image of a banned user."

                @dataclass
                class Option:
                    name: str = "name"
                    name_desc: str = "The name of the banned user."
                option = Option()
            showimg = Showimg()
        banlist = Banlist()
    command = Command()

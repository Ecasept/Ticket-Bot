# Silas Bot Copilot Instructions

This document provides guidance for AI assistants to effectively contribute to the Silas Bot codebase.

## Architecture Overview

The bot is built with Python using the `py-cord` library. The project follows a feature-based architecture.

- **`main.py`**: The main entry point which simply runs `src/bot.py`.
- **`src/bot.py`**: The core of the bot. It handles client initialization, event listeners (`on_ready`), and registers all commands and persistent UI views.
- **`src/features/`**: This is where the main logic for each bot feature resides. Each subdirectory (e.g., `ticket/`, `giveaway/`, `team/`) corresponds to a major feature.
- **`src/database/`**: Contains all database-related code. The bot uses a SQLite database (`db/tickets.db`).
  - `database.py`: Manages the database connection.
  - Other files (`ticket.py`, `giveaway.py`, etc.) act as Data Access Objects (DAOs) for specific tables, abstracting the SQL queries.
- **`src/utils.py`**: A crucial file containing shared utility functions for common tasks like creating embeds, handling errors, checking permissions, and fetching configuration from the database.
- **`src/res/`**: This directory manages the bot's text resources and localization.
  - `res.py`: Implements the dynamic resource loading system. It provides three key objects: `R` (for runtime, guild-specific strings), `RD` (for default strings used in decorators), and `RL` (for py-cord's localization dictionaries).
  - `lang/de.py`: Contains all user-facing German strings, organized in nested dataclasses. This is the primary source of truth for text.
  - `utils.py`: Contains UI helper functions for creating UI components with late-bound callbacks.
- **`src/constants.py`**: Defines non-localizable constants (`C`) like colors, static configuration values, and database keys.
- **`src/error.py`**: Defines custom error classes (`Error`, `We`, `Ce`) used throughout the application for consistent error handling.

## Features Overview

The bot has a rich set of features designed for server management, primarily focused on a ticket system.

- **Ticket System**: The core feature. Users can create tickets for support, applications, etc.
  - **`ticket`**: Handles the main ticket lifecycle (closing, reopening, etc.).
  - **`ticket_menu`**: Manages the menu from which users create tickets.
  - **`category`**: Allows configuration of different ticket categories with custom questions and roles.
  - **`setup`**: Commands for server administrators to set up the ticket system.
- **Giveaways**: A complete giveaway system (`giveaway/`) allowing moderators to create, manage, and draw winners for giveaways.
- **Moderation**:
  - **`banlist`**: A feature to manage a server-specific ban list.
  - **`timeout`**: Commands for timing out users.
- **Team Management**: The `team.py` feature allows managing teams.

## Key Developer Workflows

### Adding a New Feature

New features should be modular and self-contained within a new directory under `src/features/`. A feature is typically split into three logical parts:

1.  **`command.py` - The Command Interface**:

    - This file defines the user-facing slash commands.
    - It should contain a `setup_..._command(bot)` function that registers the commands using `@bot.slash_command(...)`.
    - The command functions themselves should be lightweight, primarily responsible for parsing user input and calling the core logic in `<feature>.py`.

2.  **`<feature>.py` - The Core Logic**:

    - This file contains the main business logic of the feature. For example, `giveaway.py` handles the creation of giveaway embeds, drawing winners, and interacting with the database.
    - Functions in this file should be independent of the Discord command context where possible, taking parameters like `guild`, `user`, etc., instead of the `interaction` object directly. This improves testability and reusability.

3.  **`button.py` - Ticket Menu Integration**:
    - This file defines discord buttons and views emulating the functionality that the command interface provides for integrating this feature into the ticket menu.
    - For commands relying extensively on command options, this file might provide a lot of views and selections.
    - The core logic and views shared by the command and ticket menu should still reside in `<feature>.py`
    - The button needs to be registered in `src/features/ticket_menu/ticket_menu.py`

**Workflow Example:**

1.  **Create a feature directory**: `src/features/my_feature/`.
2.  **Define the core logic and shared ui**: Create `src/features/my_feature/my_feature.py` with the main functions.
3.  **Define the command**: Create `src/features/my_feature/command.py`. Inside, define a `setup_my_feature_command(bot)` function. This function will contain the slash command definitions. The command handlers will call the logic in `my_feature.py`.
4.  **Define Ticket Menu Integration**: Create `src/features/my_feature/button.py` with discord views and/or buttons.
5.  **Register the command**: In `src/bot.py`, import your new setup function and call it before `bot.run(TOKEN)`.
6.  **Register persistent views**: If your feature uses persistent views (e.g., a panel that should work after a restart), you **must** add an instance of the view in the `on_ready` event in `src/bot.py` using `bot.add_view(MyView())`.

### Interacting with the Database

- **NEVER** write raw SQL queries in feature files.
- **DAO Pattern**: The database is managed through a single global object `db` defined in `src/database/__init__.py`. This object holds several "manager" classes (DAOs) for different tables (e.g., `TicketManager`, `GiveawayManager`).
- **How to Use**: To perform a database operation, import the `db` object and call the relevant manager's method.
- **Example**: To get a ticket, use `from src.database import db` and then call `db.ticket.get_ticket(ticket_id)`.
- The database connection and migrations (from `db/migrations/`) are handled automatically by the `Database` class in `src/database/database.py`.

### Writing Database Migrations

When the database schema changes, a new migration file must be created. The system is designed to apply these migrations automatically.

1.  **Create a new migration file**: In the `db/migrations/` directory, create a new SQL file named `v<N>.sql`, where `N` is the next sequential version number. For example, if the last migration was `v8.sql`, the new one will be `v9.sql`.
2.  **Update the user version**: In `src/database/database.py`, increment the `USER_VERSION` constant to match the new version number.
3.  **Write the migration script**:
    - All migrations must be written in raw SQL.
    - Wrap your entire migration in a `BEGIN TRANSACTION;` and `COMMIT;` block to ensure atomicity.
    - For complex data transformations (e.g., changing a column type or structure), follow this pattern:
      1.  Create a new table with the desired schema (e.g., `tickets_new`).
      2.  Use `INSERT INTO ... SELECT ...` to copy and transform data from the old table to the new one.
      3.  Drop the old table (`DROP TABLE tickets;`).
      4.  Rename the new table to the original name (`ALTER TABLE tickets_new RENAME TO tickets;`).

### Error Handling

The project has a standardized error handling pattern.

- When a recoverable error occurs (e.g., user input error), return an `Error` object from `src/error.py`.
- Use the `handle_error(interaction, err)` function from `src/utils.py` to send a standardized, ephemeral error message to the user.
- For permission checks, use `verify_mod_or_admin(interaction, error_message)`, which handles the check and error response internally.

**Example:**

```python
# In a command function
from src.utils import get_member, handle_error
from src.error import We
from src.res import R

member, err = get_member(interaction.guild, user_id)
if err:
    await handle_error(interaction, err)
    return
# ... proceed with member object
```

### Using UI Components (Views)

- For interactive components like buttons and menus, use `discord.ui.View`.
- Define your view class in the relevant feature directory.
- For views that need to persist after a bot restart (like a ticket panel), you **must** add an instance of it in the `on_ready` event in `src/bot.py` using `bot.add_view(MyView())`.
- For creating UI components with callbacks that need access to localized resources, use the helpers in `src/res/utils.py`, especially the `@late` decorator.

### Resource and String Management

The bot uses a sophisticated, multi-layered system for handling strings and constants to support localization and maintain clean code.

#### `src/constants.py` - Static Values

- All static, non-localizable values (like embed colors, fixed durations, or database keys) are defined in the `Constants` class within `src/constants.py`.
- These are accessed via the `C` alias: `from src.constants import C`.

#### `src/res/` - Localized Strings

- All user-facing strings are managed by the resource system in `src/res/`. The strings themselves are defined in language-specific files like `src/res/lang/de.py`.
- There are three ways to access strings:

1.  **`R` (Runtime Resources)**: For use inside command handlers, views, and other runtime contexts where a `guild_id` is available. It dynamically provides strings in the guild's configured language.

    - **Usage**: You **must** initialize it at the start of your async task (e.g., a command function).
    - **Example**:

      ```python
      from src.res import R

      async def my_non_interaction_task(guild)
          await R.init(guild.id)
        # Now you can use R to access localized strings
        ping_command_name = R.command.ping.name
      ```

    - There are multiple instances where R resources are typically used and need to be initialized:

      - Slash command definitions
        - Not needed when using `RD` and `RL` as shown below
      - Slash command body
        - Automatically done when using the correct subclassed bot object
      - Button callback definitions and body
        - Only automatically done when using `@late` decorator and `LateView` subclass (inherits from `InitView`)
      - If manually adding an item with `self.add_item` and setting the callback, the callback **must** initialize `R` manually.

2.  **`RD` (Default Resources)**: For use in places where a guild context is not available, such as in command decorators. It always returns strings in the bot's default language (German).

    - **Usage**: Use it for command names, descriptions, and option descriptions.
    - **Example**:

      ```python
      from src.res import RD, RL

      @bot.slash_command(
          name=RD.command.ping.name,
          description=RD.command.ping.desc,
          name_localizations=RL.command.ping.name,
          description_localizations=RL.command.ping.desc
      )
      async def ping(interaction: discord.Interaction):
          # ...
      ```

3.  **`RL` (Localized Resources)**: Provides dictionaries mapping locales to strings, specifically for `py-cord`'s `name_localizations` and `description_localizations` parameters in decorators. This allows Discord clients to show command details in the user's language.

    - **Usage**: Use it alongside `RD` in command definitions as shown in the example above.

#### Late Views

When creating a discord view class and using @discord.ui.button or similiar decorators and passing in resource strings, they are evaluated when the class is defined. We want them to be evaluated when the request arrives so that the resource object is correctly initialized. Therefore refrain from using @discord.ui annotations and use the @late decorator from `src.res`:

```
class MyClass(LateView):
	@late(lambda: button(name=R.bla))
```

#### New Strings and Localization

New strings should be added to the appropriate language file in `src/res/lang/`. The structure is organized in nested dataclasses, so you can easily find or add new strings. Under no circumstances should you use the old flat hierarchy!

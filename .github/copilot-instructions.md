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
- **`src/res.py`**: Defines constants for resource strings (`R`) and configuration values (`C`) like colors and titles. This is the single source of truth for user-facing text.
- **`src/error.py`**: Defines custom error classes (`Error`, `We`, `Ce`) used throughout the application for consistent error handling.

## Key Developer Workflows

### Adding a New Command

1.  **Create a feature directory**: If it doesn't exist, create a new directory under `src/features/your_feature_name/`.
2.  **Define the command**: Create a `command.py` file in your feature directory. Inside, define a setup function, e.g., `setup_my_feature_command(bot)`. This function will contain the slash command definitions (`@bot.slash_command(...)`).
3.  **Register the command**: In `src/bot.py`, import your new setup function and call it before `bot.run(TOKEN)`.

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

### Constants and Strings

- All user-facing strings (messages, titles, descriptions) should be defined as constants in `src/res.py` and accessed via `R.your_string_name`.
- All color codes and other static configuration values should be in `src/res.py` under the `C` class.
- This makes maintenance and future localization much easier.

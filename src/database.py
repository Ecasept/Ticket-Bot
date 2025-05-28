"""
Database module for managing ticket data using SQLite.
Provides the Database class for CRUD operations on tickets.
"""
import sqlite3
import os
import datetime
from src.utils import C, logger
import re


USER_VERSION = 5

# Register adapter and converter for datetime


def adapt_datetime_iso(val: datetime.datetime):
    """Adapt datetime.datetime to ISO 8601 string."""
    return val.isoformat()


def convert_datetime(val):
    """Convert ISO 8601 string to datetime.datetime."""
    return datetime.datetime.fromisoformat(val.decode())


sqlite3.register_adapter(datetime.datetime, adapt_datetime_iso)
sqlite3.register_converter("timestamp", convert_datetime)
sqlite3.register_converter("boolean", lambda val: bool(int(val.decode())))


class DatabaseError(Exception):
    """Custom exception for database errors."""
    pass


def replace_migration_placeholders(migration_script: str) -> str:
    """
    Replace placeholders in the migration script with actual values.

    Placeholders are in the format `{{name|default_value}}`.
    If the environment variable `name` is set, the placeholder is replaced with its value.
    If not, it is replaced with `default_value`.
    This is useful for migrating databases to a schema with new columns.

    Args:
        migration_script (str): The migration script with placeholders.
    Returns:
        str: The migration script with placeholders replaced.
    """
    regex = re.compile(r'{{(.*?)\|(.*?)}}')
    placeholders = re.findall(regex, migration_script)
    for (ph, default) in placeholders:
        value = os.getenv(ph.strip())
        if value is None:
            value = default.strip()
        migration_script = migration_script.replace(
            f'{{{{{ph}|{default}}}}}', value)
    return migration_script


class Ticket:
    def __init__(self, channel_id: str, category: str, user_id: str, assignee_id: str | None, archived: bool, created_at: datetime.datetime, close_at: datetime.datetime | None):
        def is_string_digit(s: str) -> bool:
            """Check if a string is a digit."""
            return isinstance(s, str) and s.isdigit()

        if not is_string_digit(channel_id):
            raise DatabaseError("channel_id has invalid format")
        if category not in ["application", "report", "support"]:
            raise DatabaseError("category has invalid format")
        if not is_string_digit(user_id):
            raise DatabaseError("user_id has invalid format")
        if not is_string_digit(assignee_id) and assignee_id is not None:
            raise DatabaseError("assignee_id has invalid format")
        if not isinstance(archived, bool):
            raise DatabaseError("archived has invalid format")
        if not isinstance(created_at, datetime.datetime):
            raise DatabaseError("created_at has invalid format")
        if not (isinstance(close_at, datetime.datetime) or close_at is None):
            raise DatabaseError("close_at has invalid format")
        self.channel_id = channel_id
        self.category = category
        self.user_id = user_id
        self.assignee_id = assignee_id
        self.archived = archived
        self.created_at = created_at
        self.close_at = close_at


class Database:
    """
    Handles SQLite database operations for ticket management.
    """

    def _migrate(self, backup: bool, from_version: int = None, ):
        """
        Apply migrations to the database schema.
        v0 is the initial version of the database.
        If you want to create the database from scratch, set `from_version` to -1.
        Args:
            from_version (int): The version to start migrations from. If None, uses the current user version. Can be set to -1 to create the database from scratch.
            backup (bool): Whether to create a backup of the database before migration.
        """
        if from_version is None:
            # Get the current user version
            current_user_version = self.connection.execute(
                "PRAGMA user_version"
            ).fetchone()[0]
        else:
            current_user_version = from_version

        if current_user_version == USER_VERSION:
            logger.info(
                "db", f"Database version is up to date (v{USER_VERSION}).")
            return

        if backup:
            # Create a backup of the database
            backup_filename = self.filename + ".bak"
            if os.path.exists(backup_filename):
                os.remove(backup_filename)
            backup_conn = sqlite3.connect(backup_filename)
            with backup_conn:
                self.connection.backup(backup_conn)

        # Incrementally apply migrations until the current user version matches the latest one
        while current_user_version < USER_VERSION:
            mig_name = f"db/migrations/v{current_user_version + 1}.sql"
            with open(mig_name, 'r') as f:
                migration = f.read()
            migration = replace_migration_placeholders(migration)
            self.connection.executescript(migration)
            current_user_version += 1
        # Set the user version to the latest version
        self.connection.execute(
            "PRAGMA user_version = {}".format(USER_VERSION)
        )
        self.connection.commit()
        logger.info("db", f"Database migrated to version {USER_VERSION}.")

    def __init__(self, filename: str):
        """
        Initialize the Database object.
        Args:
            filename (str): Path to the SQLite database file.
        """
        self.filename = filename
        self.connection = None

    def connect(self):
        """
        Connect to the database. If it doesn't exist, create it.
        Apply migrations if necessary.
        """
        if not os.path.exists(self.filename):
            self._create_database(self.filename)
        self.connection = sqlite3.connect(
            self.filename, detect_types=sqlite3.PARSE_DECLTYPES
        )
        self.cursor = self.connection.cursor()
        logger.info("db", f"Database {self.filename} opened.")
        self._migrate(True)

    def _create_database(self, filename: str):
        """
        Create the database file and tables using the schema file.
        Args:
            filename (str): Path to the new database file.
        """
        # Create the database file
        with open(filename, 'w') as f:
            pass
        # Create the tables
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()

        # Create the tables using the migrations
        self._migrate(False, -1)

        self.connection.commit()
        self.connection.close()
        logger.info("db", f"Database {filename} created.")

    def close(self):
        """
        Close the database connection.
        """
        self.connection.close()
        logger.info("db", "Database connection closed.")

    def create_ticket(self, channel_id: str, category: str, user_id: str, assignee_id: str, archived: bool = False, close_at: datetime.datetime | None = None):
        """
        Create a new ticket record in the database.
        Args:
            channel_id (str): Discord channel ID for the ticket.
            category (str): Ticket category ('application' or 'report').
            user_id (str): ID of the user who created the ticket.
            assignee_id (str): ID of the user assigned to the ticket.
            archived (bool): Whether the ticket is archived or not. Defaults to False.
            close_at (datetime.datetime | None): When the ticket should be closed. Defaults to None.
        Returns:
            str: The channel_id of the created ticket.
        """
        self.cursor.execute(
            "INSERT INTO tickets (channel_id, category, user_id, assignee_id, archived, close_at) VALUES (?, ?, ?, ?, ?, ?)",
            (channel_id, category, user_id, assignee_id, archived, close_at)
        )
        self.connection.commit()
        logger.info("db",
                    f"Ticket {channel_id} created with category {category}, user {user_id}, assignee {assignee_id}, archived status {archived}, and close_at {close_at}.")
        return channel_id

    def get_ticket(self, channel_id: str):
        """
        Retrieve a ticket by its channel_id.
        Args:
            channel_id (str): Discord channel ID for the ticket.
        Returns:
            Ticket or None: Ticket data if found, else None.
        """
        self.cursor.execute(
            "SELECT channel_id, category, user_id, assignee_id, archived, created_at, close_at FROM tickets WHERE channel_id = ?", (channel_id,))
        ticket = self.cursor.fetchone()
        if ticket:
            cid, category, user_id, assignee_id, archived, created_at, close_at = ticket
            return Ticket(
                channel_id=cid,
                category=category,
                user_id=user_id,
                assignee_id=assignee_id,
                archived=archived,
                created_at=created_at,
                close_at=close_at
            )
        else:
            return None

    def update_ticket(self, channel_id: str, **fields):
        """
        Update one or more fields of a ticket.
        Args:
            channel_id (str): Discord channel ID for the ticket.
            **fields: Keyword arguments for fields to update.
                     Supported fields: assignee_id, archived, close_at
        """
        if not fields:
            raise ValueError("At least one field must be provided for update")

        set_clauses = []
        values = []
        for field, value in fields.items():
            if field not in ['assignee_id', 'archived', 'close_at']:
                raise ValueError(f"Invalid field '{field}' for ticket update")
            set_clauses.append(f"{field} = ?")
            values.append(value)

        # Add channel_id to the end for the WHERE clause
        values.append(channel_id)

        query = f"UPDATE tickets SET {', '.join(set_clauses)} WHERE channel_id = ?"
        self.cursor.execute(query, values)
        self.connection.commit()

        # Log the update
        field_updates = ", ".join([f"{k}={v}" for k, v in fields.items()])
        logger.info("db", f"Ticket {channel_id} updated: {field_updates}")

    def delete_ticket(self, channel_id: str):
        """
        Delete a ticket by its channel_id.
        Args:
            channel_id (str): Discord channel ID for the ticket.
        """
        self.cursor.execute(
            "DELETE FROM tickets WHERE channel_id = ?", (channel_id,)
        )
        self.connection.commit()
        logger.info("db", f"Ticket {channel_id} deleted.")

    def get_overdue_tickets(self, time: datetime.datetime) -> list[str]:
        """
        Finds tickets where `close_at` is less than `now` and `archived` is `FALSE`,
        and returns their channel_ids.
        Args:
            time (datetime.datetime): The time to compare against ticket `close_at` times.
        Returns:
            list[str]: A list of channel_ids for the overdue tickets.

        """
        query = """
            SELECT channel_id
            FROM tickets
            WHERE close_at < ? AND archived = FALSE;
        """
        self.cursor.execute(query, (time,))
        overdue_ticket_ids = [row[0] for row in self.cursor.fetchall()]
        if overdue_ticket_ids:
            logger.info(
                "db", f"Found {len(overdue_ticket_ids)} overdue tickets: {', '.join(overdue_ticket_ids)}")
        return overdue_ticket_ids

    # === Constants ===

    def get_constant(self, key: str, guild: int) -> str | None:
        """
        Get a constant value from the database.
        Args:
            key (str): Key of the constant.
            guild (int): Guild ID for the constant.
        Returns:
            str or None: Constant value if found, else None.
        """
        self.cursor.execute(
            "SELECT value FROM constants WHERE key = ? AND guild_id = ?", (key, guild))
        constant = self.cursor.fetchone()
        if constant:
            return constant[0]
        else:
            return None

    def set_constant(self, key: str, value: str, guild: int):
        """
        Set a constant value in the database.
        Args:
            key (str): Key of the constant.
            value (str): Value to set.
            guild (int): Guild ID for the constant.
        """
        self.cursor.execute(
            "INSERT OR REPLACE INTO constants (key, guild_id, value) VALUES (?, ?, ?)",
            (key, guild, value)
        )
        self.connection.commit()
        logger.info("db", f"Constant {key} set to {value} for guild {guild}.")


db = Database(C.db_file)

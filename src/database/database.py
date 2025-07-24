"""
Database module for managing ticket data using SQLite.
Provides the Database class for CRUD operations on tickets.
"""
import sqlite3
import os
import datetime
from .application_ban import ApplicationBanManager
from .constant import ConstantManager
from .giveaway import GiveawayManager
from .ticket import TicketManager
from .ticket_category import TicketCategoryManager
from .banlist import BanlistManager
from src.utils import logger
from src.res import C
import re


USER_VERSION = 11

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


class Database:
    """
    Handles SQLite database operations for ticket management.
    """

    giveaway: GiveawayManager | None = None
    ticket: TicketManager | None = None
    constant: ConstantManager | None = None
    ab: ApplicationBanManager | None = None
    tc: TicketCategoryManager | None = None
    banlist: BanlistManager | None = None

    def _migrate(self, backup: bool, from_version: int = None):
        """
        Apply migrations to the database schema.
        v0 is the initial version of the database.
        If you want to create the database from scratch, set `from_version` to -1.
        Args:
            from_version (int): The version to start migrations from. If None, uses the current user version. Can be set to -1 to create the database from scratch.
            backup (bool): Whether to create a backup of the database before migration.
        """
        if from_version is None:
            current_user_version = self.connection.execute(
                "PRAGMA user_version").fetchone()[0]
        else:
            current_user_version = from_version

        if current_user_version == USER_VERSION:
            logger.info(f"Database version is up to date (v{USER_VERSION}).")
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
        logger.info(f"Database migrated to version {USER_VERSION}.")

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
        logger.info(f"Database {self.filename} opened.")
        self._migrate(True)
        self._init_components()

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
        logger.info(f"Database {filename} created.")

    def close(self):
        """
        Close the database connection.
        """
        if self.connection is not None:
            self.connection.close()
        logger.info("Database connection closed.")

    def _init_components(self):
        """
        Initialize the components of the database.
        This should be called after connecting to the database.
        """
        self.giveaway = GiveawayManager(self.connection)
        self.ticket = TicketManager(self.connection)
        self.constant = ConstantManager(self.connection)
        self.ab = ApplicationBanManager(self.connection)
        self.tc = TicketCategoryManager(self.connection)
        self.banlist = BanlistManager(self.connection)

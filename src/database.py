"""
Database module for managing ticket data using SQLite.
Provides the Database class for CRUD operations on tickets.
"""
import sqlite3
import os

from src.utils import C, logger


USER_VERSION = 1


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
            with open(self.filename, 'rb') as original_file:
                with open(backup_filename, 'wb') as backup_file:
                    backup_file.write(original_file.read())
            logger.info("db", f"Backup created: {backup_filename}")

        # Incrementally apply migrations until the current user version matches the latest one
        while current_user_version < USER_VERSION:
            mig_name = f"db/migrations/v{current_user_version + 1}.sql"
            with open(mig_name, 'r') as f:
                migration = f.read()
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

    def connect(self):
        """
        Connect to the database. If it doesn't exist, create it.
        Apply migrations if necessary.
        """
        if not os.path.exists(self.filename):
            self._create_database(self.filename)
        self.connection = sqlite3.connect(self.filename)
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

    def create_ticket(self, channel_id: str, category: str, user_id: str, assignee_id: str, archived: bool = False):
        """
        Create a new ticket record in the database.
        Args:
            channel_id (str): Discord channel ID for the ticket.
            category (str): Ticket category ('application' or 'report').
            user_id (str): ID of the user who created the ticket.
            assignee_id (str): ID of the user assigned to the ticket.
            archived (bool): Whether the ticket is archived or not. Defaults to False.
        Returns:
            str: The channel_id of the created ticket.
        """
        self.cursor.execute(
            "INSERT INTO tickets (channel_id, category, user_id, assignee_id, archived) VALUES (?, ?, ?, ?, ?)",
            (channel_id, category, user_id, assignee_id, archived)
        )
        self.connection.commit()
        logger.info("db",
                    f"Ticket {channel_id} created with category {category}, user {user_id}, assignee {assignee_id}, and archived status {archived}.")
        return channel_id

    def get_ticket(self, channel_id: str):
        """
        Retrieve a ticket by its channel_id.
        Args:
            channel_id (str): Discord channel ID for the ticket.
        Returns:
            dict or None: Ticket data if found, else None.
        """
        self.cursor.execute(
            "SELECT channel_id, category, user_id, assignee_id, archived, created_at FROM tickets WHERE channel_id = ?", (channel_id,))
        ticket = self.cursor.fetchone()
        if ticket:
            return {
                "channel_id": ticket[0],
                "category": ticket[1],
                "user_id": ticket[2],
                "assignee_id": ticket[3],
                "archived": ticket[4],
                "created_at": ticket[5]
            }
        else:
            return None

    def update_ticket_assignee(self, channel_id: str, assignee_id: str):
        """
        Update the assignee of a ticket.
        Args:
            channel_id (str): Discord channel ID for the ticket.
            assignee_id (str): New assignee's user ID.
        """
        self.cursor.execute(
            "UPDATE tickets SET assignee_id = ? WHERE channel_id = ?",
            (assignee_id, channel_id)
        )
        self.connection.commit()
        logger.info(
            "db", f"Ticket {channel_id} assignee updated to {assignee_id}.")

    def update_ticket_archived(self, channel_id: str, archived: bool):
        """
        Update the archived status of a ticket.
        Args:
            channel_id (str): Discord channel ID for the ticket.
            archived (bool): New archived status.
        """
        self.cursor.execute(
            "UPDATE tickets SET archived = ? WHERE channel_id = ?",
            (archived, channel_id)
        )
        self.connection.commit()
        logger.info(
            "db", f"Ticket {channel_id} archived status updated to {archived}.")

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


db = Database(C.db_file)

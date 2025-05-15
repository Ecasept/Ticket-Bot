import sqlite3
import os

from utils import C, logger


class Database:
    def __init__(self, filename: str):
        self.filename = filename

    def connect(self):
        """Connect to the database. If it doesn't exist, create it."""
        if not os.path.exists(self.filename):
            self.create_database(self.filename)
        self.connection = sqlite3.connect(self.filename)
        self.cursor = self.connection.cursor()
        logger.info(f"Database {self.filename} opened.")

    def create_database(self, filename: str):
        """Create the database file and tables"""
        # Create the database file
        with open(filename, 'w') as f:
            pass
        # Create the tables
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()
        with open(C.db_schema_file, 'r') as f:
            schema = f.read()
        self.cursor.executescript(schema)
        self.connection.commit()
        self.connection.close()
        logger.info(f"Database {filename} created.")

    def close(self):
        """Close the database connection."""
        self.connection.close()
        logger.info("Database connection closed.")

    def create_ticket(self, channel_id: str, category: str, user_id: str, assignee_id: str):
        """Create a new ticket."""
        self.cursor.execute(
            "INSERT INTO tickets (channel_id, category, user_id, assignee_id) VALUES (?, ?, ?, ?)",
            (channel_id, category, user_id, assignee_id)
        )
        self.connection.commit()
        logger.info(
            f"Ticket {channel_id} created with category {category}, user {user_id}, and assignee {assignee_id}.")
        return channel_id

    def get_ticket(self, channel_id: str):
        """Get a ticket by its channel_id."""
        self.cursor.execute(
            "SELECT channel_id, category, user_id, assignee_id, created_at FROM tickets WHERE channel_id = ?", (channel_id,))
        ticket = self.cursor.fetchone()
        if ticket:
            return {
                "channel_id": ticket[0],
                "category": ticket[1],
                "user_id": ticket[2],
                "assignee_id": ticket[3],
                "created_at": ticket[4]
            }
        else:
            return None

    def update_ticket_assignee(self, channel_id: str, assignee_id: str):
        """Update the assignee of a ticket."""
        self.cursor.execute(
            "UPDATE tickets SET assignee_id = ? WHERE channel_id = ?",
            (assignee_id, channel_id)
        )
        self.connection.commit()
        logger.info(f"Ticket {channel_id} assignee updated to {assignee_id}.")

    def delete_ticket(self, channel_id: str):
        """Delete a ticket by its channel_id."""
        self.cursor.execute(
            "DELETE FROM tickets WHERE channel_id = ?", (channel_id,)
        )
        self.connection.commit()
        logger.info(f"Ticket {channel_id} deleted.")


db = Database(C.db_file)

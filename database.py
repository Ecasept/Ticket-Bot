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

    def get_ticket(self, ticket_id: int):
        """Get a ticket by its ID."""
        self.cursor.execute(
            "SELECT * FROM tickets WHERE id = ?", (ticket_id,))
        ticket = self.cursor.fetchone()
        if ticket:
            return {
                "id": ticket[0],
                "category": ticket[1],
                "assigned_id": ticket[2],
                "archived": ticket[3]
            }
        else:
            return None

    def create_ticket(self, category: str, assigned_id: str, archived: str):
        """Create a new ticket."""
        self.cursor.execute(
            "INSERT INTO tickets (category, assigned_id, archived) VALUES (?, ?, ?)",
            (category, assigned_id, archived)
        )
        self.connection.commit()
        ticket_id = self.cursor.lastrowid
        logger.info(f"Ticket {ticket_id} created.")
        return ticket_id

    def update_ticket(self, ticket_id: int, category: str, assigned_id: str, archived: str):
        """Update a ticket."""
        self.cursor.execute(
            "UPDATE tickets SET category = ?, assigned_id = ?, archived = ? WHERE id = ?",
            (category, assigned_id, archived, ticket_id)
        )
        self.connection.commit()
        logger.info(f"Ticket {ticket_id} updated.")

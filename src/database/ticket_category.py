"""
Database manager for ticket categories.
Handles CRUD operations for custom ticket categories, their permissions, and questions.
"""
import datetime
from typing import List, Dict, Optional, Tuple
from .other import DatabaseError
from src.utils import logger


class TicketCategory:
    """
    Represents a custom ticket category.

    Args:
        id (int): The category ID.
        name (str): The category name.
        emoji (str): The category emoji.
        description (str): The category description.
        guild_id (int): The Discord guild ID this category belongs to.
    """

    def __init__(self, id: int, name: str, emoji: str, description: str, guild_id: int):
        self.id = id
        self.name = name
        self.emoji = emoji
        self.description = description
        self.guild_id = guild_id


class TicketCategoryManager:
    """
    Manages ticket categories in the database.
    """

    def __init__(self, connection):
        """
        Initialize the TicketCategoryManager with a database connection.
        Args:
            connection: SQLite database connection object.
        """
        self.connection = connection
        self.cursor = connection.cursor()

    def create_category(self, name: str, emoji: str, description: str, guild_id: int) -> int:
        """
        Create a new ticket category.

        Args:
            name (str): The category name.
            emoji (str): The category emoji.
            description (str): The category description.
            guild_id (int): The Discord guild ID.

        Returns:
            int: The ID of the created category.
        """
        self.cursor.execute(
            "INSERT INTO ticket_categories (name, emoji, description, guild_id) VALUES (?, ?, ?, ?)",
            (name, emoji, description, guild_id)
        )
        self.connection.commit()
        category_id = self.cursor.lastrowid

        logger.info(
            f"Ticket category '{name}' created with ID {category_id} for guild {guild_id}")
        return category_id

    def get_category(self, category_id: int) -> Optional[TicketCategory]:
        """
        Get a ticket category by ID.

        Args:
            category_id (int): The category ID.

        Returns:
            TicketCategory: The category data if found, else None.
        """
        self.cursor.execute(
            "SELECT id, name, emoji, description, guild_id FROM ticket_categories WHERE id = ?",
            (category_id,)
        )
        result = self.cursor.fetchone()
        if result:
            return TicketCategory(*result)
        return None

    def get_categories_for_guild(self, guild_id: int) -> List[TicketCategory]:
        """
        Get all ticket categories for a guild.

        Args:
            guild_id (int): The Discord guild ID.

        Returns:
            List[TicketCategory]: List of categories for the guild.
        """
        self.cursor.execute(
            "SELECT id, name, emoji, description, guild_id FROM ticket_categories WHERE guild_id = ? ORDER BY name",
            (guild_id,)
        )
        results = self.cursor.fetchall()
        return [TicketCategory(*result) for result in results]

    def update_category(self, category_id: int, **fields):
        """
        Update one or more fields of a ticket category.

        Args:
            category_id (int): The category ID.
            **fields: Keyword arguments for fields to update.
                     Supported fields: name, emoji, description
        """
        if not fields:
            raise ValueError("At least one field must be provided for update")

        valid_fields = ['name', 'emoji', 'description']
        set_clauses = []
        values = []

        for field, value in fields.items():
            if field not in valid_fields:
                raise ValueError(
                    f"Invalid field '{field}' for category update")
            set_clauses.append(f"{field} = ?")
            values.append(value)

        values.append(category_id)

        query = f"UPDATE ticket_categories SET {', '.join(set_clauses)} WHERE id = ?"
        self.cursor.execute(query, values)
        self.connection.commit()

        field_updates = ", ".join([f"{k}={v}" for k, v in fields.items()])
        logger.info(f"Ticket category {category_id} updated: {field_updates}")

    def delete_category(self, category_id: int) -> bool:
        """
        Delete a ticket category and all associated data.

        Args:
            category_id (int): The category ID.

        Returns:
            bool: True if the category was deleted, False if it didn't exist.
        """
        # Check if category exists
        if not self.get_category(category_id):
            return False

        # Delete the category (CASCADE will handle roles and questions)
        self.cursor.execute(
            "DELETE FROM ticket_categories WHERE id = ?", (category_id,))
        self.connection.commit()

        logger.info(f"Ticket category {category_id} deleted")
        return True

    def add_role_permission(self, category_id: int, role_id: int):
        """
        Add a role permission to a category.

        Args:
            category_id (int): The category ID.
            role_id (int): The Discord role ID.
        """
        # Check if permission already exists
        self.cursor.execute(
            "SELECT 1 FROM ticket_category_roles WHERE category_id = ? AND role_id = ?",
            (category_id, role_id)
        )
        if self.cursor.fetchone():
            return  # Permission already exists

        self.cursor.execute(
            "INSERT INTO ticket_category_roles (category_id, role_id) VALUES (?, ?)",
            (category_id, role_id)
        )
        self.connection.commit()

        logger.info(f"Role {role_id} added to category {category_id}")

    def remove_role_permission(self, category_id: int, role_id: int):
        """
        Remove a role permission from a category.

        Args:
            category_id (int): The category ID.
            role_id (int): The Discord role ID.
        """
        self.cursor.execute(
            "DELETE FROM ticket_category_roles WHERE category_id = ? AND role_id = ?",
            (category_id, role_id)
        )
        self.connection.commit()

        logger.info(f"Role {role_id} removed from category {category_id}")

    def get_role_permissions(self, category_id: int) -> List[int]:
        """
        Get all role IDs that have permission to use a category.

        Args:
            category_id (int): The category ID.

        Returns:
            List[int]: List of role IDs.
        """
        self.cursor.execute(
            "SELECT role_id FROM ticket_category_roles WHERE category_id = ?",
            (category_id,)
        )
        return [row[0] for row in self.cursor.fetchall()]

    def set_category_roles(self, category_id: int, role_ids: List[int]):
        """
        Set the role permissions for a category (replaces existing).

        Args:
            category_id (int): The category ID.
            role_ids (List[int]): List of role IDs to set permissions for.
        """
        # Remove existing permissions
        self.cursor.execute(
            "DELETE FROM ticket_category_roles WHERE category_id = ?",
            (category_id,)
        )

        # Add new permissions
        for role_id in role_ids:
            self.cursor.execute(
                "INSERT INTO ticket_category_roles (category_id, role_id) VALUES (?, ?)",
                (category_id, role_id)
            )

        self.connection.commit()
        logger.info(
            f"Category {category_id} role permissions set to: {role_ids}")

    def add_question(self, category_id: int, question: str) -> int:
        """
        Add a question to a category.

        Args:
            category_id (int): The category ID.
            question (str): The question text.

        Returns:
            int: The ID of the created question.
        """
        self.cursor.execute(
            "INSERT INTO ticket_category_questions (category_id, question) VALUES (?, ?)",
            (category_id, question)
        )
        self.connection.commit()
        question_id = self.cursor.lastrowid

        logger.info(f"Question added to category {category_id}: {question}")
        return question_id

    def remove_question(self, question_id: int):
        """
        Remove a question from a category.

        Args:
            question_id (int): The question ID.
        """
        self.cursor.execute(
            "DELETE FROM ticket_category_questions WHERE id = ?",
            (question_id,)
        )
        self.connection.commit()

        logger.info(f"Question {question_id} removed")

    def get_questions(self, category_id: int) -> List[Tuple[int, str]]:
        """
        Get all questions for a category.

        Args:
            category_id (int): The category ID.

        Returns:
            List[Tuple[int, str]]: List of (question_id, question_text) tuples.
        """
        self.cursor.execute(
            "SELECT id, question FROM ticket_category_questions WHERE category_id = ? ORDER BY id",
            (category_id,)
        )
        return self.cursor.fetchall()

    def set_questions(self, category_id: int, questions: List[str]):
        """
        Set the questions for a category (replaces existing).

        Args:
            category_id (int): The category ID.
            questions (List[str]): List of question texts.
        """
        # Remove existing questions
        self.cursor.execute(
            "DELETE FROM ticket_category_questions WHERE category_id = ?",
            (category_id,)
        )

        # Add new questions
        for question in questions:
            self.cursor.execute(
                "INSERT INTO ticket_category_questions (category_id, question) VALUES (?, ?)",
                (category_id, question)
            )

        self.connection.commit()
        logger.info(f"Category {category_id} questions updated")

    def user_can_use_category(self, category_id: int, user_role_ids: List[int]) -> bool:
        """
        Check if a user can use a category based on their roles.

        Args:
            category_id (int): The category ID.
            user_role_ids (List[int]): List of role IDs the user has.

        Returns:
            bool: True if the user can use the category, False otherwise.
        """
        # Get required role IDs for this category
        required_role_ids = self.get_role_permissions(category_id)

        # If no roles are required, anyone can use it
        if not required_role_ids:
            return True

        # Check if user has any of the required roles
        return any(role_id in required_role_ids for role_id in user_role_ids)

    def get_categories_for_user(self, guild_id: int, user_role_ids: List[int]) -> List[TicketCategory]:
        """
        Get all categories a user can access based on their roles.

        Args:
            guild_id (int): The Discord guild ID.
            user_role_ids (List[int]): List of role IDs the user has.

        Returns:
            List[TicketCategory]: List of categories the user can access.
        """
        all_categories = self.get_categories_for_guild(guild_id)
        return [
            category for category in all_categories
            if self.user_can_use_category(category.id, user_role_ids)
        ]

    def get_ticket_count(self, category_id: int) -> int:
        """
        Get the number of active tickets for a category.

        Args:
            category_id (int): The category ID.

        Returns:
            int: The number of active tickets in this category.
        """
        self.cursor.execute(
            "SELECT COUNT(*) FROM tickets WHERE category_id = ? AND archived = 0",
            (category_id,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else 0

"""
Category management package for custom ticket categories.
"""
from .command import setup_category_command
from .menu import CategoryButton
from .questions import CategoryQuestionsModal

# Feature modules
from .create import handle_create_category
from .edit import handle_edit_categories
from .remove import handle_remove_category
from .shared import get_category_details, create_category_embed

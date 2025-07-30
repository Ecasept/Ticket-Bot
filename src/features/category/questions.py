"""
Question management for ticket categories.
Handles category-specific questions and their collection during ticket creation.
"""
import discord
from typing import List, Tuple, Dict
from src.res import R
from src.res.utils import LateView, button, late
from src.constants import C
from src.utils import create_embed, logger, handle_error
from src.database import db
from src.error import Ce


class CategoryQuestionsModal(discord.ui.Modal):
    """Modal that shows category-specific questions when creating a ticket."""

    def __init__(self, category, questions: List[Tuple]):
        """
        Initialize the modal with category questions.

        Args:
            category: The ticket category object.
            questions: List of question tuples (id, question_text).
        """
        super().__init__(title=R.feature.category.questions.modal.title % category.name)
        self.category = category
        self.questions = questions
        self.answers = {}

        # Discord modals support up to 5 input fields
        # If there are more questions, we'll need to handle them differently
        for i, (question_id, question_text) in enumerate(questions[:5]):
            input_field = discord.ui.InputText(
                label=R.feature.category.questions.modal.question_label % (
                    i + 1),
                placeholder=question_text,
                required=True,
                style=discord.InputTextStyle.long if len(
                    question_text) > 50 else discord.InputTextStyle.short,
                max_length=1000
            )

            # Store the question ID in the input field for later reference
            input_field.custom_id = f"question_{question_id}"
            self.add_item(input_field)

    async def callback(self, interaction: discord.Interaction):
        """Handle the modal submission."""
        await R.init(interaction.guild_id)
        # Collect answers from all input fields
        for item in self.children:
            if isinstance(item, discord.ui.InputText) and item.custom_id.startswith("question_"):
                question_id = int(item.custom_id.split("_")[1])
                self.answers[question_id] = item.value

        # Defer the response - the ticket creation will be handled elsewhere
        await interaction.response.defer()

    def get_formatted_answers(self) -> str:
        """
        Get a formatted string of all answers.

        Returns:
            str: Formatted answers for display in the ticket.
        """
        if not self.answers:
            return R.feature.category.questions.modal.no_answers

        formatted_lines = []
        for question_id, answer in self.answers.items():
            # Find the question text
            question_text = R.feature.category.questions.modal.unknown_question
            for q_id, q_text in self.questions:
                if q_id == question_id:
                    question_text = q_text
                    break

            formatted_lines.append(f"**{question_text}**\n{answer}")

        return "\n\n".join(formatted_lines)

    def get_answers_dict(self) -> Dict[int, str]:
        """
        Get the answers as a dictionary.

        Returns:
            Dict[int, str]: Mapping of question_id to answer.
        """
        return self.answers.copy()


class QuestionAddModal(discord.ui.Modal):
    """Modal for adding a single question to a category."""

    def __init__(self, category):
        super().__init__(
            title=R.feature.category.questions.add_modal.title % category.name)
        self.category = category

        self.question = discord.ui.InputText(
            label=R.feature.category.questions.add_modal.question_label,
            placeholder=R.feature.category.questions.add_modal.question_placeholder,
            required=True,
            style=discord.InputTextStyle.long,
            max_length=500
        )

        self.add_item(self.question)

    async def callback(self, interaction: discord.Interaction):
        """Handle the modal submission."""
        await R.init(interaction.guild_id)
        await interaction.response.defer()


class QuestionsReplaceModal(discord.ui.Modal):
    """Modal for replacing all questions for a category."""

    def __init__(self, category):
        super().__init__(
            title=R.feature.category.questions.replace_modal.title % category.name)
        self.category = category

        # Get current questions to pre-fill
        current_questions = db.tc.get_questions(category.id)
        current_text = "\n".join(
            [q[1] for q in current_questions]) if current_questions else ""

        self.questions = discord.ui.InputText(
            label=R.feature.category.questions.replace_modal.questions_label,
            placeholder=R.feature.category.questions.replace_modal.questions_placeholder,
            required=False,
            style=discord.InputTextStyle.long,
            value=current_text,
            max_length=2000
        )

        self.add_item(self.questions)

    async def callback(self, interaction: discord.Interaction):
        """Handle the modal submission."""
        await R.init(interaction.guild_id)
        await interaction.response.defer()


class CategoryQuestionEditView(LateView):
    """View for editing questions for a category."""

    def __init__(self, category):
        super().__init__(timeout=300)
        self.category = category

    @late(lambda: button(label=R.category_question_add, style=discord.ButtonStyle.primary, emoji="➕"))
    async def add_question(self, button: discord.ui.Button, interaction: discord.Interaction):
        modal = QuestionAddModal(self.category)
        await interaction.response.send_modal(modal)
        await modal.wait()

        if modal.question and modal.question.value.strip():
            db.tc.add_question(self.category.id, modal.question.value)

            embed = create_embed(
                R.feature.category.questions.edit_view.add_success_desc % (
                    self.category.name, modal.question.value),
                color=C.success_color,
                title=R.feature.category.questions.edit_view.add_success_title
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

    @late(lambda: button(label=R.category_questions_replace_all, style=discord.ButtonStyle.secondary, emoji="🔄"))
    async def replace_questions(self, button: discord.ui.Button, interaction: discord.Interaction):
        modal = QuestionsReplaceModal(self.category)
        await interaction.response.send_modal(modal)
        await modal.wait()

        if modal.questions is not None:
            # Parse questions (one per line)
            question_list = []
            if modal.questions.value and modal.questions.value.strip():
                question_list = [
                    q.strip() for q in modal.questions.value.split('\n') if q.strip()]

            db.tc.set_questions(self.category.id, question_list)

            embed = create_embed(
                R.feature.category.questions.edit_view.replace_success_desc % (
                    self.category.name, len(question_list)),
                color=C.success_color,
                title=R.feature.category.questions.edit_view.replace_success_title
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

    @late(lambda: button(label=R.category_questions_delete_all, style=discord.ButtonStyle.danger, emoji="🗑️"))
    async def clear_questions(self, button: discord.ui.Button, interaction: discord.Interaction):
        db.tc.set_questions(self.category.id, [])

        embed = create_embed(
            R.feature.category.questions.edit_view.clear_success_desc % self.category.name,
            color=C.success_color,
            title=R.feature.category.questions.edit_view.clear_success_title
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


class CategoryQuestionsMultiModal:
    """
    Handler for categories with more than 5 questions.
    Manages multiple modals if needed.
    """

    def __init__(self, category, questions: List[Tuple]):
        self.category = category
        self.questions = questions
        self.all_answers = {}
        self.current_modal_index = 0

        # Split questions into groups of 5
        self.question_groups = []
        for i in range(0, len(questions), 5):
            self.question_groups.append(questions[i:i+5])

    async def show_first_modal(self, interaction: discord.Interaction):
        """Show the first modal in the sequence."""
        if not self.question_groups:
            # No questions, proceed directly
            await interaction.response.defer()
            return

        modal = CategoryQuestionsModal(
            self.category,
            self.question_groups[self.current_modal_index]
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        # Collect answers from this modal
        self.all_answers.update(modal.get_answers_dict())

        # If there are more question groups, show next modal
        if self.current_modal_index + 1 < len(self.question_groups):
            self.current_modal_index += 1
            # We need to handle this through a follow-up interaction
            # For now, we'll limit to 5 questions per category
            # This could be extended with a more complex flow if needed

    def get_all_answers(self) -> Dict[int, str]:
        """Get all collected answers."""
        return self.all_answers.copy()

    def get_formatted_answers(self) -> str:
        """Get formatted string of all answers."""
        if not self.all_answers:
            return R.feature.category.questions.modal.no_answers

        formatted_lines = []
        for question_id, answer in self.all_answers.items():
            # Find the question text
            question_text = R.feature.category.questions.modal.unknown_question
            for q_id, q_text in self.questions:
                if q_id == question_id:
                    question_text = q_text
                    break

            formatted_lines.append(f"**{question_text}**\n{answer}")

        return "\n\n".join(formatted_lines)

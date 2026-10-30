"""Command handlers for PROсрочка bot."""
from telegram.ext import CommandHandler

from ..services.export import format_project_table
from ..services.projects import ProjectService
from ..utils.formatting import format_project_list
from ..utils.keyboards import make_project_type_keyboard

project_service = ProjectService()


async def start_command(update, context):
    """Handle /start command."""
    await update.message.reply_text(
        "Добро пожаловать в PROсрочка! 📋\n\n"
        "Я помогу вам не забыть о важных сроках.\n\n"
        "Выберите тип проекта:",
        reply_markup=make_project_type_keyboard()
    )


async def projects_command(update, context):
    """Handle /projects command."""
    chat_id = update.message.chat_id
    projects = await project_service.get_projects_by_chat(chat_id)
    await update.message.reply_text(format_project_list(projects))


async def table_command(update, context):
    """Handle /table command — show project table."""
    chat_id = update.message.chat_id
    projects = await project_service.get_projects_by_chat(chat_id)
    table = format_project_table(projects)
    await update.message.reply_text(table)


def setup_commands(app):
    """Set up all command handlers."""
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("projects", projects_command))
    app.add_handler(CommandHandler("table", table_command))

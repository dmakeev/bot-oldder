"""Command handlers for PROсрочка bot."""
from telegram.ext import CommandHandler
from ..utils.keyboards import make_project_type_keyboard


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
    # TODO: Get projects from service and display
    await update.message.reply_text("Пока нет проектов.")


def setup_commands(app):
    """Set up all command handlers."""
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("projects", projects_command))

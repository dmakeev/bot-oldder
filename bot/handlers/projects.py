"""Project handlers for PROсрочка bot."""
from telegram.ext import CallbackQueryHandler


async def project_type_handler(update, context):
    """Handle project type selection."""
    query = update.callback_query
    await query.answer()

    project_type = query.data.replace("project_", "")
    # TODO: Start conversation for creating project
    await query.edit_message_text(f"Создание проекта: {project_type}")


def setup_project_handlers(app, date_calc, calendar):
    """Set up project handlers."""
    app.add_handler(CallbackQueryHandler(project_type_handler, pattern="^project_"))

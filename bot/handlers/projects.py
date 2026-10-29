"""Project handlers for PROсрочка bot."""
from telegram.ext import CallbackQueryHandler, MessageHandler, filters, ConversationHandler

from ..services.projects import ProjectService
from ..services.reminders import ReminderService

# Conversation states
PROJECT_TYPE, PROJECT_NAME, CASE_NUMBER = range(3)
CUSTOM_NAME, CUSTOM_TEXT, CUSTOM_DATE = range(10, 13)

project_service = ProjectService()
reminder_service = ReminderService()


async def project_type_handler(update, context):
    """Handle project type selection."""
    query = update.callback_query
    await query.answer()

    project_type = query.data.replace("project_", "")
    context.user_data['project_type'] = project_type

    # Custom reminder — different flow (no case number)
    if project_type == "custom":
        await query.edit_message_text("Введите название напоминания:")
        return CUSTOM_NAME

    await query.edit_message_text(
        f"Создание проекта: {project_type}\n\nВведите название дела:"
    )
    return PROJECT_NAME


async def project_name_handler(update, context):
    """Handle project name input."""
    context.user_data['project_name'] = update.message.text
    await update.message.reply_text("Введите номер дела (например, А123-456/2026):")
    return CASE_NUMBER


async def case_number_handler(update, context):
    """Handle case number input and create project."""
    case_number = update.message.text

    project_id = await project_service.create_project(
        chat_id=update.message.chat_id,
        name=context.user_data['project_name'],
        case_number=case_number,
        project_type=context.user_data['project_type']
    )

    # Clear user data
    context.user_data.clear()

    await update.message.reply_text(
        f"✅ Проект создан!\nНазвание: {context.user_data.get('project_name', '—')}\n"
        f"Дело: {case_number}"
    )
    return ConversationHandler.END


async def custom_name_handler(update, context):
    """Handle custom reminder name input."""
    context.user_data['project_name'] = update.message.text
    await update.message.reply_text("Введите текст напоминания:")
    return CUSTOM_TEXT


async def custom_text_handler(update, context):
    """Handle custom reminder text input."""
    context.user_data['reminder_text'] = update.message.text
    await update.message.reply_text(
        "Введите дату (ДД.ММ.ГГГГ) или нажмите Отмена для отмены"
    )
    return CUSTOM_DATE


async def custom_date_handler(update, context):
    """Handle custom reminder date input."""
    from datetime import datetime
    try:
        date_str = update.message.text
        reminder_date = datetime.strptime(date_str, "%d.%m.%Y")
        # Create project
        project_id = await project_service.create_project(
            chat_id=update.message.chat_id,
            name=context.user_data['project_name'],
            project_type="custom",
            reminder_text=context.user_data['reminder_text'],
            reminder_date=reminder_date.isoformat()
        )
        context.user_data.clear()
        await update.message.reply_text(
            f"✅ Напоминание создано!\nНазвание: {context.user_data.get('project_name', '—')}\n"
            f"Текст: {context.user_data.get('reminder_text', '—')}\n"
            f"Дата: {date_str}"
        )
    except ValueError:
        await update.message.reply_text("Неверный формат даты. Используйте ДД.ММ.ГГГГ")
        return CUSTOM_DATE
    return ConversationHandler.END


def setup_project_handlers(app, date_calc, calendar):
    """Set up project handlers."""
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(project_type_handler, pattern="^project_")],
        states={
            PROJECT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, project_name_handler)],
            CASE_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, case_number_handler)],
            CUSTOM_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, custom_name_handler)],
            CUSTOM_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, custom_text_handler)],
            CUSTOM_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, custom_date_handler)],
        },
        fallbacks=[]
    )
    app.add_handler(conv_handler)

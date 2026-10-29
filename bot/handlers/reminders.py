"""Reminder handlers for PROсрочка bot."""
from telegram.ext import CallbackQueryHandler

from ..services.reminders import ReminderService


reminder_service = ReminderService()


async def reminder_done_handler(update, context):
    """Handle 'Done' button."""
    query = update.callback_query
    await query.answer()

    reminder_id = int(query.data.replace("done_", ""))
    await reminder_service.mark_reminder_done(reminder_id)
    await query.edit_message_text("✅ Выполнено")


async def reminder_cancel_handler(update, context):
    """Handle 'Cancel' button."""
    query = update.callback_query
    await query.answer()

    reminder_id = int(query.data.replace("cancel_", ""))
    await reminder_service.mark_reminder_cancelled(reminder_id)
    await query.edit_message_text("❌ Отменено")


async def reminder_mute_handler(update, context):
    """Handle 'Mute' button."""
    query = update.callback_query
    await query.answer()

    reminder_id = int(query.data.replace("mute_", ""))
    await reminder_service.mark_reminder_muted(reminder_id)
    await query.edit_message_text("🔕 Больше не напоминать")


def setup_reminder_handlers(app, date_calc, calendar):
    """Set up reminder handlers."""
    app.add_handler(CallbackQueryHandler(reminder_done_handler, pattern="^done_"))
    app.add_handler(CallbackQueryHandler(reminder_cancel_handler, pattern="^cancel_"))
    app.add_handler(CallbackQueryHandler(reminder_mute_handler, pattern="^mute_"))

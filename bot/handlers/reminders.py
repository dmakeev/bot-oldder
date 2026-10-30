"""Reminder handlers for PROсрочка bot."""
import logging

from telegram.ext import CallbackQueryHandler

from ..services.reminders import ReminderService

logger = logging.getLogger(__name__)

reminder_service = ReminderService()


async def reminder_done_handler(update, context):
    """Handle 'Done' button."""
    query = update.callback_query
    await query.answer()

    try:
        reminder_id = query.data.replace("done_", "")
    except (AttributeError, ValueError):
        await query.edit_message_text("❌ Неверный формат данных.")
        return

    # Verify reminder belongs to this chat
    if not await _verify_reminder_ownership(reminder_id, query.message.chat_id):
        await query.edit_message_text("❌ Это напоминание не относится к этому чату.")
        return

    try:
        await reminder_service.mark_reminder_done(reminder_id)
        await query.edit_message_text("✅ Выполнено")
    except RuntimeError as e:
        await query.edit_message_text("❌ Ошибка: " + str(e))


async def reminder_cancel_handler(update, context):
    """Handle 'Cancel' button."""
    query = update.callback_query
    await query.answer()

    try:
        reminder_id = query.data.replace("cancel_", "")
    except (AttributeError, ValueError):
        await query.edit_message_text("❌ Неверный формат данных.")
        return

    if not await _verify_reminder_ownership(reminder_id, query.message.chat_id):
        await query.edit_message_text("❌ Это напоминание не относится к этому чату.")
        return

    try:
        await reminder_service.mark_reminder_cancelled(reminder_id)
        await query.edit_message_text("❌ Отменено")
    except RuntimeError as e:
        await query.edit_message_text("❌ Ошибка: " + str(e))


async def reminder_mute_handler(update, context):
    """Handle 'Mute' button."""
    query = update.callback_query
    await query.answer()

    try:
        reminder_id = query.data.replace("mute_", "")
    except (AttributeError, ValueError):
        await query.edit_message_text("❌ Неверный формат данных.")
        return

    if not await _verify_reminder_ownership(reminder_id, query.message.chat_id):
        await query.edit_message_text("❌ Это напоминание не относится к этому чату.")
        return

    try:
        await reminder_service.mark_reminder_muted(reminder_id)
        await query.edit_message_text("🔕 Больше не напоминать")
    except RuntimeError as e:
        await query.edit_message_text("❌ Ошибка: " + str(e))


async def _verify_reminder_ownership(reminder_id, chat_id):
    """Verify that a reminder belongs to a given chat."""
    try:
        return await reminder_service.reminder_belongs_to_chat(reminder_id, chat_id)
    except Exception as e:  # noqa: BLE001
        logger.error(f"Error verifying reminder ownership: {e}")
        return False


def setup_reminder_handlers(app, date_calc, calendar):
    """Set up reminder handlers."""
    app.add_handler(CallbackQueryHandler(reminder_done_handler, pattern="^done_"))
    app.add_handler(CallbackQueryHandler(reminder_cancel_handler, pattern="^cancel_"))
    app.add_handler(CallbackQueryHandler(reminder_mute_handler, pattern="^mute_"))

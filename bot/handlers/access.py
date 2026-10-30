"""Access control handlers."""
import logging

from telegram.ext import CallbackQueryHandler, CommandHandler

from ..config import ADMIN_USER_ID
from ..services.access import AccessService

logger = logging.getLogger(__name__)

access_service = AccessService()


async def handle_start_with_access(update, context):
    """Handle /start with access control."""
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    # Check if already approved
    has = await access_service.has_access(user_id)
    if has:
        # User has access, proceed normally
        from .commands import start_command
        return await start_command(update, context)

    # Request access
    status = await access_service.request_access(user_id, chat_id)

    if status == 'approved':
        from .commands import start_command
        return await start_command(update, context)
    elif status == 'denied':
        await update.message.reply_text("❌ Нет доступа к боту.")
        return
    elif status == 'revoked':
        await update.message.reply_text("❌ Ваш доступ к боту отозван.")
        return
    else:
        # Pending
        await update.message.reply_text("⏳ Запрос на доступ отправлен администратору.")

        # Notify admin
        try:
            await context.bot.send_message(
                ADMIN_USER_ID,
                f"📬 Запрос на доступ от {update.message.from_user.first_name} "
                f"(ID: {user_id})"
            )
        except Exception as e:  # noqa: BLE001
            logger.error(f"Error notifying admin: {e}")


async def approve_user_handler(update, context):
    """Handle [Approve] button."""
    query = update.callback_query
    await query.answer()

    # Verify caller is admin
    if query.from_user.id != ADMIN_USER_ID:
        await query.edit_message_text("❌ Только администратор может одобрить доступ.")
        return

    user_id = query.data.replace("approve_", "")
    user_id = int(user_id)

    await access_service.approve_access(user_id, ADMIN_USER_ID)
    await query.edit_message_text(f"✅ Доступ для {user_id} одобрен.")


async def deny_user_handler(update, context):
    """Handle [Deny] button."""
    query = update.callback_query
    await query.answer()

    # Verify caller is admin
    if query.from_user.id != ADMIN_USER_ID:
        await query.edit_message_text("❌ Только администратор может отклонить доступ.")
        return

    user_id = query.data.replace("deny_", "")
    user_id = int(user_id)

    await access_service.deny_access(user_id)
    await query.edit_message_text(f"❌ Доступ для {user_id} отклонён.")


async def list_users_handler(update, context):
    """Handle /users command — show all users."""
    # Verify caller is admin
    if update.message.from_user.id != ADMIN_USER_ID:
        await update.message.reply_text("❌ Только администратор может просмотреть пользователей.")
        return

    users = await access_service.get_all_users()

    if not users:
        await update.message.reply_text("Нет пользователей.")
        return

    text = "👥 Пользователи:\n\n"
    for user in users:
        uid, chat_id, status, _approved_by, _approved_at = user
        status_text = {"pending": "⏳", "approved": "✅", "denied": "❌", "revoked": "🔒"}.get(status, status)
        text += f"{status_text} {uid} ({chat_id})\n"

    await update.message.reply_text(text)


def setup_access_handlers(app):
    """Set up access control handlers."""
    app.add_handler(CommandHandler("users", list_users_handler))
    app.add_handler(CallbackQueryHandler(approve_user_handler, pattern="^approve_"))
    app.add_handler(CallbackQueryHandler(deny_user_handler, pattern="^deny_"))
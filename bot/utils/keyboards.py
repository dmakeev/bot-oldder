"""Inline keyboard helpers for PROсрочка bot."""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def make_reminder_keyboard(reminder_id):
    """Create keyboard for a reminder."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Сделано", callback_data=f"done_{reminder_id}")],
        [
            InlineKeyboardButton("❌ Отменить", callback_data=f"cancel_{reminder_id}"),
            InlineKeyboardButton("🔕 Больше не напоминать", callback_data=f"mute_{reminder_id}")
        ]
    ])


def make_project_type_keyboard():
    """Create keyboard for project type selection."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Дело о банкротстве", callback_data="project_bankruptcy")],
        [InlineKeyboardButton("Обособленный спор", callback_data="project_related")],
        [InlineKeyboardButton("Арбитражный спор", callback_data="project_arbitration")],
        [InlineKeyboardButton("Своё напоминание", callback_data="project_custom")]
    ])


def make_hearing_result_keyboard():
    """Create keyboard for hearing result."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Отложено", callback_data="hearing_postponed")],
        [InlineKeyboardButton("Объявлен перерыв", callback_data="hearing_break")],
        [InlineKeyboardButton("Рассмотрено", callback_data="hearing_done")]
    ])


def make_meeting_result_keyboard():
    """Create keyboard for meeting result."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Проведено", callback_data="meeting_done")],
        [InlineKeyboardButton("Перенесено", callback_data="meeting_postponed")],
        [InlineKeyboardButton("Не состоялось", callback_data="meeting_failed")]
    ])

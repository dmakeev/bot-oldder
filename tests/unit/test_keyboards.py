"""Unit tests for keyboard helpers."""
from bot.utils.keyboards import (
    make_hearing_result_keyboard,
    make_meeting_result_keyboard,
    make_project_type_keyboard,
    make_reminder_keyboard,
)


def test_make_reminder_keyboard():
    """Test reminder keyboard creation."""
    kb = make_reminder_keyboard(42)
    assert kb is not None
    assert len(kb.inline_keyboard) == 2
    assert kb.inline_keyboard[0][0].text == "✅ Сделано"
    assert kb.inline_keyboard[0][0].callback_data == "done_42"


def test_make_project_type_keyboard():
    """Test project type keyboard creation."""
    kb = make_project_type_keyboard()
    assert kb is not None
    assert len(kb.inline_keyboard) == 4
    assert kb.inline_keyboard[0][0].text == "Дело о банкротстве"
    assert kb.inline_keyboard[0][0].callback_data == "project_bankruptcy"


def test_make_hearing_result_keyboard():
    """Test hearing result keyboard creation."""
    kb = make_hearing_result_keyboard()
    assert kb is not None
    # Has 3 buttons in separate rows
    assert len(kb.inline_keyboard) == 3
    assert kb.inline_keyboard[0][0].text == "Отложено"
    assert kb.inline_keyboard[1][0].text == "Объявлен перерыв"
    assert kb.inline_keyboard[2][0].text == "Рассмотрено"


def test_make_meeting_result_keyboard():
    """Test meeting result keyboard creation."""
    kb = make_meeting_result_keyboard()
    assert kb is not None
    # Has 3 buttons in separate rows
    assert len(kb.inline_keyboard) == 3
    assert kb.inline_keyboard[0][0].text == "Проведено"
    assert kb.inline_keyboard[1][0].text == "Перенесено"
    assert kb.inline_keyboard[2][0].text == "Не состоялось"

"""Unit tests for formatting helpers."""
from bot.utils.formatting import (
    format_project_list,
    format_reminder_text,
    format_today_summary,
)


def test_format_reminder_text_basic():
    """Test basic reminder formatting."""
    text = format_reminder_text("Срок", "Дело №1", "15.11.2026")
    assert "⏰" in text
    assert "Срок" in text
    assert "Дело №1" in text
    assert "15.11.2026" in text


def test_format_reminder_text_with_workday_note():
    """Test reminder formatting with workday note."""
    text = format_reminder_text("Срок", "Дело №1", "15.11.2026", "пн")
    assert "пн" in text


def test_format_reminder_text_no_deadline():
    """Test reminder formatting without deadline."""
    text = format_reminder_text("Срок", "Дело №1", None)
    assert "Срок:" not in text


def test_format_project_list_empty():
    """Test empty project list formatting."""
    text = format_project_list([])
    assert text == "Нет проектов."


def test_format_project_list_with_items():
    """Test project list with items."""
    projects = [
        (1, "Дело №1", "А123-456/2026"),
        (2, "Дело №2", "А789-012/2026")
    ]
    text = format_project_list(projects)
    assert "Ваши проекты:" in text
    assert "Дело №1" in text
    assert "Дело №2" in text


def test_format_today_summary_empty():
    """Test empty summary formatting."""
    text = format_today_summary([])
    assert text == "На сегодня напоминаний нет."


def test_format_today_summary_with_items():
    """Test summary with items."""
    reminders = [
        {"action": "Срок подачи иска", "deadline": "15.11.2026"}
    ]
    text = format_today_summary(reminders)
    assert "Напоминания на сегодня:" in text
    assert "Срок подачи иска" in text

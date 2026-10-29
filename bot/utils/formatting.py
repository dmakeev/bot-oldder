"""Text formatting helpers for PROсрочка bot."""


def format_reminder_text(action, project_name, deadline, workday_note=None):
    """Format reminder text."""
    text = f"⏰ {action}. {project_name}"
    if deadline:
        text += f"\nСрок: {deadline}"
    if workday_note:
        text += f" ({workday_note})"
    return text


def format_project_list(projects):
    """Format list of projects for display."""
    if not projects:
        return "Нет проектов."

    lines = ["Ваши проекты:"]
    for p in projects:
        lines.append(f"{p[0]}. {p[1]} ({p[2]})")
    return "\n".join(lines)


def format_today_summary(reminders):
    """Format today's reminder summary."""
    if not reminders:
        return "На сегодня напоминаний нет."

    lines = ["📋 Напоминания на сегодня:"]
    for r in reminders:
        lines.append(f"• {r['action']} - {r['deadline']}")
    return "\n".join(lines)

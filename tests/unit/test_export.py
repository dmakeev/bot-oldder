"""Unit tests for export service."""
from bot.services.export import format_project_table


def test_format_project_table_empty():
    """Test formatting empty project table."""
    table = format_project_table([])
    assert table == "Нет проектов."


def test_format_project_table_with_projects():
    """Test formatting project table with projects."""
    projects = [
        {
            'name': 'Дело А',
            'case_number': 'А123-456/2026',
            'type': 'bankruptcy',
            'created_at': '2026-01-15 10:00:00'
        },
        {
            'name': 'Дело Б',
            'case_number': 'А789-012/2026',
            'type': 'arbitration',
            'created_at': '2026-02-20 14:30:00'
        }
    ]

    table = format_project_table(projects)
    assert 'Дело А' in table
    assert 'Дело Б' in table
    assert 'А123-456/2026' in table
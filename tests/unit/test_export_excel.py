"""Unit tests for Excel export service."""
import pytest
import tempfile
import os
from bot.services.export import export_to_excel, format_project_table


def test_export_to_excel_basic():
    """Test basic Excel export."""
    data = [
        {"name": "Project A", "status": "active"},
        {"name": "Project B", "status": "completed"},
    ]

    content = export_to_excel(data, "test.xlsx")
    assert isinstance(content, bytes)
    assert len(content) > 0

    # Write to temp file and verify
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
        f.write(content)
        temp_path = f.name

    try:
        # Verify it's a valid xlsx by reading headers
        with open(temp_path, 'rb') as f:
            header = f.read(4)
            assert header == b'PK\x03\x04'  # ZIP file header (xlsx is a zip)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_export_to_excel_empty():
    """Test Excel export with empty data."""
    content = export_to_excel([], "empty.xlsx")
    assert isinstance(content, bytes)
    assert len(content) > 0


def test_format_project_table_empty():
    """Test formatting empty project table."""
    result = format_project_table([])
    assert result == "Нет проектов."


def test_format_project_table_single():
    """Test formatting table with single project."""
    projects = [
        {
            "name": "Дело А",
            "case_number": "А123-456/2026",
            "type": "bankruptcy",
            "created_at": "2026-01-15 10:00:00"
        }
    ]

    result = format_project_table(projects)
    assert "Дело А" in result
    assert "А123-456/2026" in result
    assert "bankruptcy" in result
    assert "2026-01-15" in result


def test_format_project_table_multiple():
    """Test formatting table with multiple projects."""
    projects = [
        {
            "name": "Дело А",
            "case_number": "А123-456/2026",
            "type": "bankruptcy",
            "created_at": "2026-01-15 10:00:00"
        },
        {
            "name": "Дело Б",
            "case_number": "А789-012/2026",
            "type": "arbitration",
            "created_at": "2026-02-20 14:30:00"
        }
    ]

    result = format_project_table(projects)
    assert "Дело А" in result
    assert "Дело Б" in result
    assert result.count("|") > 10  # Multiple rows


def test_format_project_table_truncation():
    """Test that long values are truncated."""
    projects = [
        {
            "name": "A very long project name that should be truncated",
            "case_number": "A very long case number that should be truncated",
            "type": "bankruptcy",
            "created_at": "2026-01-15 10:00:00"
        }
    ]

    result = format_project_table(projects)
    assert "..." in result
    # Name should be truncated to 30 chars + ...
    lines = result.split("\n")
    data_line = lines[2]
    # Check that the name part is not the full original
    assert len(data_line.split("|")[2].strip()) < 50
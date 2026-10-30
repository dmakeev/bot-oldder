"""Export service for PROсрочка bot."""
import io

import xlsxwriter


def export_to_excel(data: list[dict], filename: str) -> bytes:
    """Export data to Excel file.

    Args:
        data: List of dicts to export
        filename: Output filename

    Returns:
        Excel file content as bytes
    """
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # Write headers
    headers = list(data[0].keys()) if data else []
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # Write data
    for row, item in enumerate(data, 1):
        for col, header in enumerate(headers):
            worksheet.write(row, col, item.get(header, ""))

    workbook.close()
    return output.getvalue()


def format_project_table(projects: list[dict]) -> str:
    """Format projects as a text table."""
    if not projects:
        return "Нет проектов."

    # Build header
    lines = ["| Название | Дело | Тип | Создан |"]
    lines.append("|----------|------|-----|--------|")

    for p in projects:
        name = p.get('name', '')
        case = p.get('case_number', '')
        ptype = p.get('type', '')
        created = p.get('created_at', '')

        # Truncate long values
        name = name[:30] + "..." if len(name) > 30 else name
        case = case[:20] + "..." if len(case) > 20 else case

        lines.append(f"| {name} | {case} | {ptype} | {created[:10] if created else '—'} |")

    return "\n".join(lines)
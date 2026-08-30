#!/usr/bin/env python
"""Load employees from Excel and return as list of dicts."""

import sys
from pathlib import Path

# Add parent to path so we can import from utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config
from utils.excel_reader import load_copy, sv

# Column indices (0-based) from CLAUDE.md
COLS = {
    'phone': 3,
    'status': 11,
    'nation': 14,
    'kafala': 15,
    'region': 16,
    'category': 18,
    'name': 20,
    'job': 21,
    'salary': 23,
}


def load_employees(excel_path=None, status_filter='على قوة العمل'):
    """
    Load employees from Excel.

    Args:
        excel_path: Path to Excel file (default: from config)
        status_filter: Filter by status column (default: 'على قوة العمل')

    Returns:
        List of dicts {name, job, region, phone, salary, ...}
    """
    excel_path = excel_path or Config.EXCEL_SOURCES['employees']

    try:
        wb = load_copy(excel_path)
        ws = wb['data']
    except Exception as e:
        print(f"[ERROR] Error loading {excel_path}: {e}", file=sys.stderr)
        return []

    employees = []
    for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=False), start=2):
        try:
            # Check status filter
            if len(row) > COLS['status']:
                status = sv(row[COLS['status']].value)
                if status_filter and status != status_filter:
                    continue

            emp = {
                'id': row_idx - 1,  # Simple ID based on row number
                'name': sv(row[COLS['name']].value),
                'job': sv(row[COLS['job']].value),
                'phone': sv(row[COLS['phone']].value),
                'region': sv(row[COLS['region']].value),
                'salary': sv(row[COLS['salary']].value),
                'nation': sv(row[COLS['nation']].value),
                'kafala': sv(row[COLS['kafala']].value),
                'category': sv(row[COLS['category']].value),
                'status': status,
            }

            # Only add if name is not empty
            if emp['name']:
                employees.append(emp)
        except (IndexError, ValueError) as e:
            print(f"[WARN] Skipping row {row_idx}: {e}", file=sys.stderr)
            continue

    wb.close()
    return employees


if __name__ == '__main__':
    employees = load_employees()
    print(f"[OK] Loaded {len(employees)} employees")

    # Show sample
    if employees:
        sample = employees[0]
        print(f"\nSample employee:")
        for key, val in sample.items():
            print(f"  {key}: {val}")

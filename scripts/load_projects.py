#!/usr/bin/env python
"""Load projects from Excel and return as list of dicts."""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config
from utils.excel_reader import load_copy, sv

# Column indices (0-based) from CLAUDE.md
COLS = {
    'po': 9,
    'active': 10,
    'name': 12,
    'district': 16,
    'region': 17,
    'contractor': 18,
    'shared': 19,
    're_general': 21,
    'state': 23,
    'start_date': 24,
    'end_date': 25,
    'type': 28,
    'value': 29,
}


def load_projects(excel_path=None, active_filter='yes', state_filter=None):
    """
    Load projects from Excel.

    Args:
        excel_path: Path to Excel file (default: from config)
        active_filter: Filter by active column (default: 'yes')
        state_filter: Filter by state column (optional, e.g., 'تحت التنفيذ')

    Returns:
        List of dicts {name, po, region, contractor, ...}
    """
    excel_path = excel_path or Config.EXCEL_SOURCES['projects']

    try:
        wb = load_copy(excel_path)
        ws = wb['pro']
    except Exception as e:
        print(f"[ERROR] Error loading {excel_path}: {e}", file=sys.stderr)
        return []

    projects = []
    for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=False), start=2):
        try:
            # Check active filter
            if len(row) > COLS['active']:
                active = sv(row[COLS['active']].value).lower()
                if active_filter and active != active_filter:
                    continue

            # Check state filter (optional)
            if state_filter and len(row) > COLS['state']:
                state = sv(row[COLS['state']].value)
                if state != state_filter:
                    continue

            proj = {
                'id': row_idx - 1,  # Simple ID based on row number
                'name': sv(row[COLS['name']].value),
                'po': sv(row[COLS['po']].value),
                'region': sv(row[COLS['region']].value),
                'contractor': sv(row[COLS['contractor']].value),
                'district': sv(row[COLS['district']].value),
                're_general': sv(row[COLS['re_general']].value),
                'state': sv(row[COLS['state']].value),
                'start_date': sv(row[COLS['start_date']].value),
                'end_date': sv(row[COLS['end_date']].value),
                'type': sv(row[COLS['type']].value),
                'value': sv(row[COLS['value']].value),
                'active': sv(row[COLS['active']].value),
                'shared': sv(row[COLS['shared']].value),
            }

            # Only add if name is not empty
            if proj['name']:
                projects.append(proj)
        except (IndexError, ValueError) as e:
            print(f"[WARN] Skipping row {row_idx}: {e}", file=sys.stderr)
            continue

    wb.close()
    return projects


if __name__ == '__main__':
    projects = load_projects()
    print(f"[OK] Loaded {len(projects)} projects")

    # Show sample
    if projects:
        sample = projects[0]
        print(f"\nSample project:")
        for key, val in sample.items():
            print(f"  {key}: {val}")

    # Show breakdown by state
    states = {}
    for proj in projects:
        state = proj['state'] or 'unknown'
        states[state] = states.get(state, 0) + 1

    print(f"\nProjects by state:")
    for state, count in sorted(states.items()):
        print(f"  {state}: {count}")

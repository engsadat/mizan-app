"""Contract amount from project DB row.

Value (col 29) is an Excel table formula reflecting القيمة (col 13).
Prefer the cached Value number; if blank or unevaluated, use القيمة.
"""
ERR_VALS = {'#REF!', '=#REF!', '#VALUE!', '#N/A', '#NAME?', '#DIV/0!', '#NULL!', '#NUM!'}

def contract_val(row):
    """Return contract SAR as float, or None if both columns are empty/invalid."""
    for idx in (29, 13):
        v = row[idx]
        if v is None or v == '':
            continue
        s = str(v).strip()
        if s in ERR_VALS or s.startswith('='):
            continue
        try:
            n = float(s.replace(',', ''))
        except (TypeError, ValueError):
            continue
        if n > 0:
            return n
    return None

"""
One-time: fill standard_rate on job_codes table.
Run from hr_webapp/: python scripts/fill_job_code_rates.py [path/to/mizan.db]
Default DB path: instance/mizan.db
"""
import sys, sqlite3
from pathlib import Path

DB_DEFAULT = Path(__file__).parent.parent / 'instance' / 'mizan.db'
db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DB_DEFAULT

CODES = {
    'أخصائي وثائق E2':     'DOC-E2',
    'أخصائي وثائق E3':     'DOC-E3',
    'حاسب كميات E2':       'QS-E2',
    'حاسب كميات E3':       'QS-E3',
    'مدير المشروع E3':      'PM-E3',
    'مراقب أمن وسلامة E2': 'HSI-E2',
    'مراقب أمن وسلامة E3': 'HSI-E3',
    'مراقب موقع E2':       'SI-E2',
    'مراقب موقع E3':       'SI-E3',
    'مساح E2':             'SV-E2',
    'مساح E3':             'SV-E3',
    'مهندس أمن وسلامة E2': 'HSE-E2',
    'مهندس أمن وسلامة E3': 'HSE-E3',
    'مهندس تخطيط E3':      'PLN-E3',
    'مهندس كهرباء E2':     'ELE-E2',
    'مهندس كهرباء E3':     'ELE-E3',
    'مهندس مقيم E3':       'RE-E3',
    'مهندس مواد وجودة E2': 'QC-E2',
    'مهندس مواد وجودة E3': 'QC-E3',
    'مهندس موقع E2':       'SITE-E2',
    'مهندس موقع E3':       'SITE-E3',
    'مهندس ميكانيكا E2':   'MECH-E2',
    'مهندس ميكانيكا E3':   'MECH-E3',
}

RATES = {
    'أخصائي وثائق E2':     10000,
    'أخصائي وثائق E3':     10000,
    'حاسب كميات E2':       15000,
    'حاسب كميات E3':       17000,
    'مدير المشروع E3':      50000,
    'مراقب أمن وسلامة E2': 11000,
    'مراقب أمن وسلامة E3': 12000,
    'مراقب موقع E2':       12000,
    'مراقب موقع E3':       12000,
    'مساح E2':             11000,
    'مساح E3':             13000,
    'مهندس أمن وسلامة E2': 18000,
    'مهندس أمن وسلامة E3': 21000,
    'مهندس تخطيط E3':      26000,
    'مهندس كهرباء E2':     19000,
    'مهندس كهرباء E3':     21000,
    'مهندس مقيم E3':       28000,
    'مهندس مواد وجودة E2': 19000,
    'مهندس مواد وجودة E3': 21000,
    'مهندس موقع E2':       19000,
    'مهندس موقع E3':       21000,
    'مهندس ميكانيكا E2':   19000,
    'مهندس ميكانيكا E3':   21000,
}

print(f'DB: {db_path}')
if not db_path.exists():
    print('ERROR: file not found'); sys.exit(1)

con = sqlite3.connect(str(db_path))
cur = con.cursor()

rows = cur.execute('SELECT id, title FROM job_codes ORDER BY title').fetchall()
print(f'Job codes in DB: {len(rows)}')
for row in rows:
    print(f'  {row[0]:3d}  {repr(row[1])}')

if not rows:
    print('ERROR: table is empty'); con.close(); sys.exit(1)

updated, not_found = 0, []
for title, rate in RATES.items():
    n = cur.execute(
        'UPDATE job_codes SET standard_rate=?, code=? WHERE title=?',
        (rate, CODES[title], title)
    ).rowcount
    if n:
        updated += 1
    else:
        not_found.append(title)

con.commit()
con.close()
print(f'\nUpdated: {updated} / {len(RATES)}')
if not_found:
    print(f'Not matched: {not_found}')

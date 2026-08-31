# Mizan — current status (2026-08-31)

Update this file at the end of every session. Then `git commit` + `git push`.
Next chat: open `mizan-app` → read `CLAUDE.md` + this file → **one** task.
Do not save status to a Claude memo.

## Live (checked 2026-08-31)

- URL: https://southmizan.pythonanywhere.com — **up** (user screenshot of A+B org-chart landing)
- CSRF: not checked this session
- Login test this session: **not checked**
- Laptop SSH: still **Permission denied** earlier today
- Org-chart landing on live had A+B icons (so a pull happened). Region cards wrapped to 2 lines (3+1). That wrap is fixed in this commit; live still needs pull.

## Code (checked 2026-08-31)

- Canonical: `engsadat/mizan-app` `master`
- This session:
  - Region cards: `grid-template-columns: repeat(4, minmax(0, 1fr))` so عسير جازان الباحة نجران stay on **one line**
  - Excel refresh (copied from `HR/source`, dated 2026-08-31):
    - `data/source/employees data source.xlsx` — still **444** on strength (575 rows)
    - `data/source/project_2026_database_ver1_updated.xlsx` — still **181** included (232 rows)
- Print org charts A/B unchanged. Do **not** run org-chart generator scripts.

## Leftovers (checked 2026-08-30)

- Do not run `scripts/test_org_charts.py` against live org HTML — it overwrote professional print charts with sample data (2 fake employees).
- Several Flask processes on `:5001` caused the UI to keep showing SQLite (4 employees) after Excel-first. `run.py` now starts with `debug=False, use_reloader=False`. One server only.
- Local SQLite `users` was empty until an admin was created with `scripts/setup_admin.py`. SQLite employees table still has a stale 4-row import; the app no longer reads it.
- `data/Organize/Office-RE.xlsx` may show a tiny local binary diff from Excel; leave it uncommitted unless the user asks.

## Product (this version)

Three home cards: الموظفون، التقارير، الإعدادات.
Settings = job codes + users. Roles: admin | editor | viewer.
**This phase: Excel is the system of record for business data.** SQLite = login / users only. Team still edits shareable `.xlsx` files. SQL conversion is later.

Employee add / edit / status in the app is **403**. Edit the Excel file, then refresh. Download: `/employees/export.xlsx`.

## Next (one task)

Pull this commit on PythonAnywhere (this laptop cannot SSH). Bash console:

```
cd /home/southMizan/mizan-app
git fetch origin
git pull origin master
git log -1 --oneline
```

Then Web tab → Reload.

Done when the four region cards are on **one line**, and live Excel is the 2026-08-31 copy (employee/project files in `data/source/`).

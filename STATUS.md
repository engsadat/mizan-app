# Mizan — current status (2026-08-31)

Update this file at the end of every session. Then `git commit` + `git push`.
Next chat: open `mizan-app` → read `CLAUDE.md` + this file → **one** task.
Do not save status to a Claude memo.

## Live (checked 2026-08-31)

- URL: https://southmizan.pythonanywhere.com — **up**
- CSRF: not checked this session
- Login test this session: **not checked**
- PythonAnywhere HEAD (user Bash): **`cfff41b`** — `Rebuild print org charts from the employee RE column.`
- Live Baha print chart verified: **سيد عبد الحميد أحمد** is under **أحمد صالح عبده** (الباحة_ وسط). Tel file `/static/org_charts/09_OrgChart_Asir_Tel.html` is present (no longer 404).
- Laptop SSH: still **Permission denied**

## Code (checked 2026-08-31)

- Canonical: `engsadat/mizan-app` `master` = `cfff41b` (laptop = GitHub = PA)
- Org-chart tree: employees Excel **column 27 (RE)** → `Office-RE.xlsx`
- A: `/reports/org-chart` — B: `/reports/org-chart-tel`
- Do **not** run `scripts/test_org_charts.py`

## Leftovers (checked 2026-08-30)

- PA `git pull` failed once because the server had a local edit of `data/source/employees data source.xlsx`. Fixed with `git checkout --` then pull. Do not `git reset --hard`.
- Several Flask processes on `:5001` caused the UI to keep showing SQLite (4 employees) after Excel-first. `run.py` now starts with `debug=False, use_reloader=False`. One server only.
- `data/Organize/Office-RE.xlsx` may show a tiny local binary diff from Excel; leave it uncommitted unless the user asks.

## Product (this version)

Three home cards: الموظفون، التقارير، الإعدادات.
Settings = job codes + users. Roles: admin | editor | viewer.
**This phase: Excel is the system of record for business data.** SQLite = login / users only.

Employee add / edit / status in the app is **403**. Edit the Excel file, then refresh. Download: `/employees/export.xlsx`.

## Next (one task)

If الموظفون or الهيكل الذكي still look old: Web tab → **Reload**, then browser **Ctrl+F5**. Print org HTML is already the new files on disk.

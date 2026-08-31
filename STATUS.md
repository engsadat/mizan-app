# Mizan — current status (2026-08-31)

Update this file at the end of every session. Then `git commit` + `git push`.
Next chat: open `mizan-app` → read `CLAUDE.md` + this file → **one** task.
Do not save status to a Claude memo.

## Live (checked 2026-08-31)

- URL: https://southmizan.pythonanywhere.com — **up**
- CSRF: not checked this session
- Login test this session: **not checked**
- PythonAnywhere last confirmed HEAD: **`cfff41b`** (print charts from RE column). This STATUS/UI commit is not on PA until the next pull.
- Live Baha print: **سيد عبد الحميد أحمد** under **أحمد صالح عبده** (الباحة_ وسط)
- Laptop SSH: **Permission denied**

## Code (checked 2026-08-31)

- Canonical: `engsadat/mizan-app` `master`
- Org-chart tree: employees Excel **column 27 (RE)** → `Office-RE.xlsx`
- **A** `/reports/org-chart` — default print, no employee phones
- **B** `/reports/org-chart-tel` — Tel print with phones; **قيد المراجعة (Under review)** on the reports cards. Still reachable; not hidden.
- Do **not** run `scripts/test_org_charts.py`

## Leftovers (checked 2026-08-30)

- PA `git pull` failed once because the server had a local edit of `data/source/employees data source.xlsx`. Fixed with `git checkout --` then pull. Do not `git reset --hard`.
- `data/Organize/Office-RE.xlsx` may show a tiny local binary diff from Excel; leave it uncommitted unless the user asks.

## Product (this version)

Three home cards: الموظفون، التقارير، الإعدادات.
Settings = job codes + users. Roles: admin | editor | viewer.
**This phase: Excel is the system of record for business data.** SQLite = login / users only.

Employee add / edit / status in the app is **403**. Edit the Excel file, then refresh. Download: `/employees/export.xlsx`.

## Next (one task)

Pull this commit on PythonAnywhere, then Web → Reload, so the قيد المراجعة badge on Tel chart B shows live.

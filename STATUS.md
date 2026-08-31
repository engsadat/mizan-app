# Mizan — current status (2026-08-31)

Update this file at the end of every session. Then `git commit` + `git push`.
Next chat: open `mizan-app` → read `CLAUDE.md` + this file → **one** task.
Do not save status to a Claude memo.

## Live (checked 2026-08-31)

- URL: https://southmizan.pythonanywhere.com — **up** (earlier today)
- CSRF: not checked this session
- Login test this session: **not checked**
- Laptop SSH: **Permission denied**
- Print org charts on live: **old snapshot** until this commit is pulled

## Code (checked 2026-08-31)

- Canonical: `engsadat/mizan-app` `master`
- Org-chart tree source: **employees Excel column 27 (RE)** matched to `Office-RE.xlsx`
- Regenerated print HTML from current Excel (user asked):
  - A: `python scripts/gen_org_chart.py` → `09–12_OrgChart_*.html`
  - B: `python scripts/gen_org_chart_tel.py` → `09–12_OrgChart_*_Tel.html` (script now writes `_Tel` names so it does not overwrite A)
- Check: سيد عبد الحميد أحمد is under **أحمد صالح عبده** (الباحة_ وسط) in both A and B
- Do **not** run `scripts/test_org_charts.py` (sample-data overwrite)

## Leftovers (checked 2026-08-30)

- Several Flask processes on `:5001` caused the UI to keep showing SQLite (4 employees) after Excel-first. `run.py` now starts with `debug=False, use_reloader=False`. One server only.
- Local SQLite `users` was empty until an admin was created with `scripts/setup_admin.py`. SQLite employees table still has a stale 4-row import; the app no longer reads it.
- `data/Organize/Office-RE.xlsx` may show a tiny local binary diff from Excel; leave it uncommitted unless the user asks.

## Product (this version)

Three home cards: الموظفون، التقارير، الإعدادات.
Settings = job codes + users. Roles: admin | editor | viewer.
**This phase: Excel is the system of record for business data.** SQLite = login / users only. Team still edits shareable `.xlsx` files. SQL conversion is later.

Employee add / edit / status in the app is **403**. Edit the Excel file, then refresh. Download: `/employees/export.xlsx`.

## Next (one task)

Pull this commit on PythonAnywhere. This laptop cannot SSH. Bash console:

```
cd /home/southMizan/mizan-app
git fetch origin
git pull origin master
git log -1 --oneline
```

Then Web tab → Reload.

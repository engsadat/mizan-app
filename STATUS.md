# Mizan — current status (2026-08-31)

Update this file at the end of every session. Then `git commit` + `git push`.
Next chat: open `mizan-app` → read `CLAUDE.md` + this file → **one** task.
Do not save status to a Claude memo.

## Live (checked 2026-08-31)

- URL: https://southmizan.pythonanywhere.com — **up** (`/auth/login` shown)
- CSRF: not checked this session
- Login test this session: **not checked** (did not submit credentials)
- Public static Asir file on live (`/static/org_charts/09_OrgChart_Asir.html`) was the **Ticket 4 grid** (stub title `المنطقة الجنوبية - NWC`, phones **and salaries**). That is the mistaken revert, not Tel.
- PythonAnywhere HEAD: **not read** (no SSH from this laptop). Files on disk match the revert `5b36ac2` / `7b002f2`, not the restored Tel charts.

## Code (checked 2026-08-31)

- Canonical: `engsadat/mizan-app` `master`
- Laptop working tree: restoring Tel print HTML, then this STATUS
- `origin/master` before this STATUS write: `7b002f2` (`docs: Update STATUS — org charts reverted to original`)
- App code history (do **not** redo, do **not** revert Tel again):
  - `5b85570` — **correct print org charts:** professional A3, office/RE layout, employee phones (`مع الاتصال`), no salaries
  - `5b36ac2` — **mistaken revert** to Ticket 4 simple grid (`cb9e97b`). Commit message said it removed phones and restored “professional print”; it did the opposite (grid + phones + salaries)
  - `7b002f2` — STATUS that recorded that revert
- This session restored the four HTML files from `5b85570`
- Local tests this session: **not run**
- Do **not** run `scripts/gen_org_charts_excel.py` or `scripts/test_org_charts.py` — they overwrite the print HTML

## Which org chart is live vs correct

| Label | SHA | What it is | Should be live? |
|---|---|---|---|
| Version A / C | `cb9e97b` / `5b36ac2` | Simple employee card grid. Stub title. Phones **and salaries**. Not an office/RE org chart | **No** |
| Version B (Tel) | `5b85570` | Professional multi-page A3 print. Offices, REs, projects, phones. No salaries. Landing page already says `مع الاتصال` | **Yes** |

User request (2026-08-30): “org chart get tel version”. Tel is the intended print design.

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

Deploy GitHub `master` (Tel print org charts) to PythonAnywhere. This laptop cannot SSH. User (or a PA Bash console) run:

```
cd /home/southMizan/mizan-app
git fetch origin
git pull origin master
git log -1 --oneline
git status -sb
```

Then Web tab → Reload `southmizan.pythonanywhere.com`.

Done when `git log -1` on the server matches GitHub `master`, and `/static/org_charts/09_OrgChart_Asir.html` title is `الهيكل التنظيمي — عسير (مع الاتصال)` (not `المنطقة الجنوبية - NWC`). Do not revert Tel.

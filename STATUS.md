# Mizan — current status (2026-08-31, updated Session 9)

**For the next Claude:** open this repo only (`engsadat/mizan-app`). Read `CLAUDE.md`, then this file. Do **one** task from **Next**. Stop. Do not use a chat memo. Do not open `hr_webapp`, `nwc-mizan-webapp`, or `Claude-Projects`.

Then `git add` + `git commit` + `git push origin master` at the end of the session.

## Live (checked 2026-08-31)

- URL: https://southmizan.pythonanywhere.com — **up**
- Server dir: `/home/southMizan/mizan-app`
- CSRF / login test: **not checked**
- Laptop SSH to PythonAnywhere: **Permission denied** — user pulls in the PA Bash console
- Last SHA the user confirmed on the server: **`cfff41b`** (print org charts rebuilt from RE column)
- GitHub `master` after this STATUS write will be a new SHA on top of **`7b47861`**
- Tel B UI badge (قيد المراجعة) is on GitHub (`0475811`+). Live shows it only after the next `git pull` + Reload
- Live Baha print (after `cfff41b`): سيد عبد الحميد أحمد is under أحمد صالح عبده (الباحة_ وسط)

## Code (checked 2026-08-31)

- Canonical: `github.com/engsadat/mizan-app` `master`
- Laptop dir: `C:\Users\engsa\OneDrive\Desktop\AI\HR\mizan`
- **Phase 1 is the Excel portal.** Excel = system of record for employees and projects. SQLite = login / users / job codes only. Do not treat SQLAlchemy `Employee` as live data. Do not wipe-and-reimport SQLite.
- Org-chart tree: employees Excel **column 27 (RE)** matched to `data/Organize/Office-RE.xlsx`
- Print **A** (default, no phones): `/reports/org-chart` → `app/static/org_charts/09–12_OrgChart_*.html`
- Print **B** Tel (phones): `/reports/org-chart-tel` → `*_Tel.html` — labelled **قيد المراجعة / Under review**. Still linked; not hidden.
- `scripts/gen_org_chart.py` writes A. `scripts/gen_org_chart_tel.py` writes `*_Tel.html` (must not overwrite A).
- **Do not** run `scripts/test_org_charts.py` — it overwrote real print HTML with sample data.

## Product (this version)

Home cards: الموظفون، التقارير، الإعدادات.  
Settings = job codes + users. Roles: `admin` | `editor` | `viewer`. Login = `User.username`.  
Employee add / edit / status in the app is **403**. Edit Excel, refresh. Download: `/employees/export.xlsx`.  
Reports already on live: BI, filter, finance, map, project dashboard, print org A/B, smart org chart.  
No SCD. No second app. No V2 rewrite. Never mention Azure.

## How the user updates data later

1. Edit Excel (employees / projects / Office-RE).
2. Copy into `data/source/` (and `data/Organize/` if Office-RE).
3. If print org charts must match: `python scripts/gen_org_chart.py` then `python scripts/gen_org_chart_tel.py`.
4. Laptop: `git add` → `git commit -m "..."` → `git push origin master`.
5. PythonAnywhere Bash:
   ```
   cd /home/southMizan/mizan-app
   git pull origin master
   git log -1 --oneline
   ```
   If pull refuses because of local Excel:  
   `git checkout -- "data/source/employees data source.xlsx"`  
   then pull again. **Never** `git reset --hard`.
6. Web tab → Reload. Browser Ctrl+F5.

Last Excel copy from HR `source/` on 2026-08-31: **444** on strength, **181** included projects (counts). Files are tracked in git.

## Leftovers (do not redo unless asked)

- Some `tests/test_employees.py` fail: tests seed SQLite; the app list reads Excel.
- `data/Organize/Office-RE.xlsx` may show a tiny local Excel binary diff — leave uncommitted unless the user asks.
- Dead copies: do not develop `nwc-mizan-webapp` or Claude-Projects Mizan V2. Close Claude-Projects PR #2 without merging.
- `C:\Users\engsa\OneDrive\Desktop\AI\mizan-app` is a second clone. Do not write specs or code there. Canonical laptop dir is this folder only.
- Do **not** add a “refresh data” button or `POST /api/refresh-data`. Excel is already read from disk on every request. No in-memory cache. Print org A/B stay stale until `gen_org_chart.py` / `gen_org_chart_tel.py`.

## Session 9 ✅ (2026-08-31)

**Completed:** Fixed employee list & side panel blank names/jobs/status.
- GitHub: `c6d81bc` (template attribute fixes)
- Tests passing: 4/5 (emp list, filter, side panel) ✅
- Live needs: `git pull` + reload on PythonAnywhere

## Next

Deploy on PythonAnywhere, then choose: investigate `test_org_chart_print_is_tel_version` OR monitor live usage.

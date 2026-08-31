# Mizan — current status (2026-08-31)

Update this file at the end of every session. Then `git commit` + `git push`.
Next chat: open `mizan-app` → read `CLAUDE.md` + this file → **one** task.
Do not save status to a Claude memo.

## Live (checked 2026-08-31)

- URL: https://southmizan.pythonanywhere.com — **up**
- CSRF / login: **not checked** this session
- PythonAnywhere last confirmed code HEAD: **`cfff41b`** (RE-column print charts)
- GitHub `master`: **`0475811`** (قيد المراجعة badge on Tel B) — needs PA pull if not pulled yet
- Laptop SSH: **Permission denied**

## Code (checked 2026-08-31)

- Canonical: `engsadat/mizan-app` `master`
- **This phase is Excel-backed, read-only for business data.** SQLite = login / users / job codes. Do not treat SQLAlchemy `Employee` tables as live.
- Org-chart tree: employees col 27 (RE) → `Office-RE.xlsx`
- A default print; B Tel **قيد المراجعة**
- Do **not** run `scripts/test_org_charts.py`

## Phase 1 review (2026-08-31)

Done as a portal: login, three home cards, employees list/search/export from Excel, reports (BI, filter, finance, map, dashboards), print org A/B, smart org chart, settings (job codes + users).

Not done / not this phase: write-from-UI to Excel or SQL, SCD, second app, V2 rewrite.

Future data update (keep this): edit Excel → copy into `data/source/` → if org print must match, run `scripts/gen_org_chart.py` then `scripts/gen_org_chart_tel.py` → `git add` / `commit` / `push` → PA `git pull origin master` → Reload.

## Leftovers

- PA local Excel edits can block `git pull` — `git checkout -- "data/source/employees data source.xlsx"` then pull. Never `reset --hard`.
- Tests last recorded: some `tests/test_employees.py` failures (tests seed SQLite; app reads Excel).
- `data/Organize/Office-RE.xlsx` tiny local Excel diff — leave uncommitted unless asked.

## Product (this version)

Three home cards: الموظفون، التقارير، الإعدادات.
Settings = job codes + users. Roles: admin | editor | viewer.
Employee add / edit / status in the app is **403**.

## Next (one task)

User to choose: (1) pull `0475811` on PA so Tel B shows قيد المراجعة, or (2) start Phase 2 only after agreeing SQL vs keep-Excel. Do not start a second Mizan.

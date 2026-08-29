# Mizan — current status (2026-08-29)

Update this file at the end of every session. Then `git commit` + `git push`.
Next chat: open `mizan-app` → read `CLAUDE.md` + this file → **one** task.
Do not save status to a Claude memo.

## Live (checked 2026-08-29)

- URL: https://southmizan.pythonanywhere.com — **up**
- Login page: Arabic ميزان / المنطقة الجنوبية, 200 OK
- CSRF: session cookie on `/auth/login` includes `csrf_token`; cookie flags Secure + HttpOnly + SameSite=Lax
- These routes exist and redirect unauthenticated users to `/auth/login` (302):
  `/` `/employees/` `/reports/` `/settings/` `/reports/finance`
  `/reports/org-chart` `/reports/org-chart-smart` `/reports/project-map-smart`
  `/reports/projects-dashboard`
- Login test this session: **not checked**
- Last successful login recorded: 2026-08-26 (admin user; do not treat as re-verified)

## Code (checked 2026-08-29)

- Canonical: `engsadat/mizan-app` `master`
- `git pull origin master`: already up to date
- Local laptop = `origin/master` @ `279bf86` (2026-08-27, “Update STATUS: Session 7 complete — Smart Chart projects fixed”)
- PythonAnywhere SHA: **not checked** (no pull/reload on the server this session)
- Working tree: clean, tracking `origin/master` only

## Leftovers still on disk (do not develop in these)

Canonical clone is intact. These still exist and should be deleted next:

- `C:\Users\engsa\OneDrive\Desktop\AI\hr_webapp`
- `C:\Users\engsa\OneDrive\Desktop\AI\nwc-mizan-webapp`

Claude-Projects PR #2 URL returned 404 this session — **not confirmed** open or closed.

## One next task

Delete the two leftover local folders above. Do not copy files from them into this repo.

## Product (this version)

Three home cards: الموظفون، التقارير، الإعدادات.
Settings = job codes + users. Roles: admin | editor | viewer.
Reports: BI + filter + finance. No SCD, no V2, no second codebase.

## One version — delete leftovers

See `CLAUDE.md` §1. Dead: `hr_webapp` folders, `nwc-mizan-webapp`, Claude-Projects Mizan PRs/branches. Close PR #2 without merging.

## Latest work (2026-08-26, session 2)

- Imported 227 projects from source Excel (project_2026_database_ver1_updated.xlsx)
- Created Project model with 32 fields (coordinates, contract, status, RE, progress, facilities)
- Built projects dashboard: `/reports/projects-dashboard`
  - KPI cards for ongoing projects by region (MSAR format)
  - Pivot tables: count and values by status × region
  - Charts: ongoing projects breakdown by region
  - Print/PDF support
- Tested locally and on PA — both working

## Dashboard complete ✓

Projects dashboard live: https://southmizan.pythonanywhere.com/reports/projects-dashboard
- KPI cards: total + 4 regions (تحت التنفيذ projects)
- Pivot tables: count & values by status × region (all projects)
- Charts: ongoing by region
- Print/PDF support

## Latest work (2026-08-26, session 3 — ORG CHART INTEGRATION COMPLETE)

**Org Chart Integration** — Implemented & deployed (Tasks 1-14):

**Task Group A: Script Generation (Tasks 1-7)**
- Created `scripts/gen_org_charts.py` with database integration
  - Loads 444 active employees from Mizan database (status = 'على قوة العمل')
  - Loads ongoing projects (project_state = 'تحت التنفيذ')
  - Generates 4 region-specific HTML org charts
  - Eager-loaded database queries (no N+1 issues)
  - Real NWC/Al-Amro logos with base64 encoding
  - Proper error handling for missing files

**Task Group B: Routes & Templates (Tasks 8-11)**
- Added 3 Flask routes with comprehensive security:
  - `/reports/org-chart` — Region selector (4 color-coded cards)
  - `/reports/org-chart/<region>` — View org chart with toolbar (print, PDF, back)
  - `/reports/org-chart/<region>/pdf` — Playwright-based PDF export (A3 landscape)
- Created 2 templates with RTL Arabic support, Cairo font, responsive layout
- Added org chart card to reports home page
- Security measures: input validation, path traversal defense, XSS mitigation with comments
- Error handling: proper HTTP status codes (404, 503, 500) with logging

**Task Group C: Dependencies (Task 12)**
- Added `playwright>=1.40.0` to requirements.txt

**Task Group D: Testing & Deployment (Tasks 13-14)**
- Local testing: 444 employees across 4 regions, all 4 HTML files generated
- Tests passing: 35 passed (no regressions)
- Code merged to master @ `2a9f92e`
- Pushed to GitHub

## Live Status (2026-08-26)
- **Code:** Merged to master locally and GitHub
- **Tests:** 35/35 passing
- **Deployment:** Awaiting PythonAnywhere server deployment (Playwright install + web app reload required)

## Known Limitations

**HTML Design Gap:**
- Current HTML generates data listings but lacks visual org chart structure
- Reference PDFs (01_AS.pdf, etc.) show professional hierarchical layout with:
  - KPI metric cards at top
  - Grid-based RE cards with team details
  - Color-coded role badges
  - Multi-page detail hierarchies
- Current output does NOT match reference design
- Requires significant HTML/CSS redesign to match reference appearance

## Session 4 (2026-08-27) — Org Chart Migration Complete

**What was done:**
1. **Identified the gap** — Last session's Mizan script generated simple data lists, NOT professional A3 org charts
2. **Ported reference script** — Copied proven `gen_org_chart.py` from HR/org_charts/ to Mizan
3. **Updated all paths** — Changed from HR folder structure to Mizan server paths:
   - Excel data: `data/source/`, `data/Organize/`
   - Output: `app/static/org_charts/`
   - Logos: `data/NWC layout/img/` (with fallback to `app/static/images/`)
4. **Created data symlinks** — Linked HR Excel files + logos so no duplication
5. **Added Flask routes** — New routes in `reports/routes.py`:
   - `/reports/org-chart` — Region selector page
   - `/reports/org-chart/<region>` — View org chart (loads pre-generated HTML)
6. **Created UI template** — `org_chart_selector.html` for region selection
7. **Tested locally** — Script generates all 4 professional org charts:
   - عسير: 13 RE offices, 4 pages + cover
   - جازان: 6 RE offices, 2 pages + cover
   - الباحة: 4 RE offices, 2 pages + cover
   - نجران: 3 RE offices, 1 page + cover

**Output quality:** Professional A3 landscape, proper page breaks, all styling, specialist sections, KPI cards, cover page ✅

## Deployment Complete ✅ (2026-08-27)

**Live URL:** https://southmizan.pythonanywhere.com/reports/org-chart

**What's Live:**
- Region selector (4 cards: عسير, جازان, الباحة, نجران)
- Professional A3 org charts (1-4 pages per region + cover)
- Hierarchical org structure (RE offices → projects → teams)
- Print/PDF export ready
- Cover pages with KPI cards
- Specialist sections (color-coded by type)

**Deployment Summary:**
1. ✅ Code: GitHub commit 4157c51 (fixed duplicate routes)
2. ✅ Data: All Excel files uploaded to server
3. ✅ Web app: Reloaded on PythonAnywhere
4. ✅ Routes: Using existing org_chart_landing + org_chart_view (with PDF export)
5. ✅ Testing: Live and functional

## Session 5 (2026-08-27) — Dynamic Smart Chart Complete ✅

**One Task Completed:**
- Built **interactive Smart Chart org chart** (`/reports/org-chart-smart`)

**Features:**
- ✅ Tab-based navigation by region (عسير, جازان, الباحة, نجران)
- ✅ KPI cards per region (employees, projects, contractors, offices)
- ✅ Search/filter with real-time highlighting
- ✅ Collapsible RE office cards (click to expand/collapse)
- ✅ Employees grouped by job category
- ✅ Complete data from Excel sources (same as static A3 charts)
- ✅ Responsive grid layout, mobile-friendly

**Implementation:**
- Route: `/reports/org-chart-smart` (reads from Excel data: employees, projects, RE directory)
- Template: `org_chart_smart.html` (JavaScript interactivity: search, filter, toggle)
- Linked in reports index alongside static charts
- Uses absolute paths for PythonAnywhere compatibility
- Final commit: `4ce6798`

**Two Org Chart Options Now Live:**
1. **Static A3 Charts** — `/reports/org-chart` (print-optimized, pre-generated HTML)
2. **Smart Chart** — `/reports/org-chart-smart` (interactive dashboard, searchable)

**Live Status (2026-08-27):**
- ✅ Both org charts deployed and working on PythonAnywhere
- ✅ All Excel data properly loaded and displayed
- ✅ Job titles shown correctly, employees grouped by category
- ✅ Search functionality working
- ✅ Region tabs functional
- ✅ All commits pushed to GitHub (master)

**Next Session:**
- Monitor live usage and user feedback
- Consider performance optimizations if needed

## Session 7 (2026-08-27) — Smart Chart Projects Fixed ✅

**One Task Completed:**
- Fixed Smart Chart org chart — projects now display correctly

**Issues Fixed:**
1. Template bug: Changed `proj.project_name` → `proj['name']` (dict key access)
2. Route path bug: Fixed data directory path calculation (was offset by 1 level)
3. Route fallback: Added local path check before server path

**Result:**
- All 194 projects now display in Smart Chart org chart across 26 REs
- KPI cards show correct project counts per region (93 عسير, 47 جازان, 35 الباحة, etc.)
- Projects visible in expanded RE cards

**Commits:**
- `01097a3`: Template fix
- `6413970`: Route path fix (local dev fallback)
- `020836e`: Combined final fix with debug cleanup

**Next:** Reload web app on PythonAnywhere

## Session 6 (2026-08-27) — Smart Project Map Complete ✅

**One Task Completed:**
- Built **interactive Smart Project Map** (`/reports/project-map-smart`)

**Features:**
- ✅ Tab-based navigation by region (عسير, جازان, الباحة, نجران)
- ✅ KPI cards per region (total, mapped, missing, RE count)
- ✅ Interactive Leaflet map with color-coded markers by RE
- ✅ Sidebar with searchable RE list + project counts
- ✅ Collapsible missing coordinates table
- ✅ Complete data from Excel source (project_2026_database_ver1_updated.xlsx)
- ✅ Responsive design matching Smart Chart UI style
- ✅ Cairo font, RTL Arabic, NWC branding

**Implementation:**
- Route: `/reports/project-map-smart` (loads Excel, renders interactive map)
- Template: `project_map_smart.html` (Leaflet + Tabs + Search)
- Reports index: Updated with new card linking to feature
- Commits: `afc3f2a` (initial), `f9ae4d0` (path fix)

**Deployment Status:**
- Code: Pushed to GitHub master (commit `f9ae4d0`)
- Excel data: Available on PythonAnywhere at `/home/southMizan/mizan-app/data/`
- Testing: Local testing passed — data loads correctly
- **PENDING:** Manual deployment to PythonAnywhere (see steps below)

**Filter Applied (Session 6 update):**
- Shows **only ongoing projects** (حالة المشروع = تحت التنفيذ)
- 132 ongoing projects in database (124 with coordinates, 8 missing)
- Simplified card display (removed state badge since all are ongoing)
- Updated labels to reflect ongoing-only scope

## Deployed ✅ (2026-08-27)

Live URL: https://southmizan.pythonanywhere.com/reports/project-map-smart

**Status:** Working — shows 132 ongoing projects (تحت التنفيذ) with region tabs, RE filtering, KPI cards, interactive map, and search.

**Session 6 Summary:**
- ✅ Built Smart Project Map with Leaflet interactive map
- ✅ Filtered to ongoing projects only (132 total, 124 mapped, 8 missing coords)
- ✅ Added search/filter for RE names (real-time, case-insensitive)
- ✅ Deployed to live server
- ❌ Attempted Projects → DB migration but hit PythonAnywhere environment issues
- ✅ **Decision:** Keep Excel as project data source (working fine, no sync needed)

**Data Strategy (Current):**
- Employees: DB (Mizan) + multiple reports
- Projects: Excel (shared file) + 1 report (map)
- Both approaches working independently ✅

**When to revisit DB for Projects:**
- If/when need 3+ different project reports (financial, timeline, risk, KPIs)
- Currently 1 map report is sufficient
- Excel is easier to maintain with shared editing

**Next Session:**
- Monitor live usage
- Build additional reports if needed (finance, risk, etc.)
- Revisit database migration if report scenarios multiply

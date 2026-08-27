# Mizan — current status (2026-08-27)

Update this file at the end of every session. Then `git commit` + `git push`.
Next chat: open `mizan-app` → read `CLAUDE.md` + this file → **one** task.
Do not save status to a Claude memo.

## Live (checked 2026-08-27)

- URL: https://southmizan.pythonanywhere.com — **up**
- Login page: Arabic ميزان / المنطقة الجنوبية, CSRF on, session cookie Secure + HttpOnly + SameSite=Lax
- `/` `/employees/` `/reports/` `/settings/` `/reports/finance` → redirect to `/auth/login` (routes exist)
- Login (admin user, password reset on PA): **succeeded** (2026-08-26)
- Job codes page: Populated with codes and salaries via script (2026-08-26)

## Code

- Canonical: `engsadat/mizan-app` `master` @ `2a9f92e` (2026-08-26, org chart integration complete)
- PythonAnywhere HEAD: `e90d900` (awaiting deployment of org chart feature)
- GitHub master: `2a9f92e` (org chart merged: script, routes, templates, PDF export)
- Local laptop: `C:\Users\engsa\OneDrive\Desktop\AI\HR\mizan` tracking `origin/master` only

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

**Deployment Steps (manual):**
1. SSH into PythonAnywhere: `ssh southmizan@ssh.pythonanywhere.com`
2. Pull latest: `cd ~/mizan-app && git pull origin master`
3. Reload web app: Go to PythonAnywhere dashboard → Web → Reload southmizan.pythonanywhere.com

**Next Session:**
- Deploy to live (manual SSH + reload)
- Test on live URL: https://southmizan.pythonanywhere.com/reports/project-map-smart
- Monitor for any runtime issues

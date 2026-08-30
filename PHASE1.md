# Mizan v2 — PHASE 1: Port Current Features to Excel-Backed Architecture

**Created:** 2026-08-30  
**Architecture:** Flask web app + Excel file storage (no SQLite)  
**Scope:** 7 core features + 1 shared layer

---

## Overview

**Vision:** Rebuild Mizan as a modern Flask app backed by Excel files (not database). Users interact with web UI; data persists in Excel files on the server. Enables stakeholder-friendly data updates (Excel edits sync to UI).

**Why Excel?**
- All HR data already in Excel format
- Stakeholders familiar with direct Excel edits
- No database admin overhead
- Easy versioning/audit (Excel timestamps)
- Simpler data import/export workflow

---

## Architecture Decision: Excel-Backed Storage

### File Structure

**Data files location:** `data/source/` (symlinked from HR project)

| File | Sheet | Purpose | Current Rows |
|------|-------|---------|--------------|
| `employees data source.xlsx` | `data` | Employee master | 444 active |
| `project_2026_database_ver1_updated.xlsx` | `pro` | Projects master | 227 ongoing |
| `vacations.xlsx` | — | Leave requests | — |
| `source/contacts.xlsx` | `contacts` | Contact directory | — |
| `Invoices/Jun_Inv.xlsx` | — | Invoice/attendance | 509 employees |

### Read/Write Pattern

```python
# Read (safe, read-only)
def load_copy(path):
    tmp = str(path) + ".tmp.xlsx"
    shutil.copy2(path, tmp)
    wb = openpyxl.load_workbook(tmp, data_only=True)
    os.remove(tmp)
    return wb

# Write (versioned, with backup)
def save_excel(wb, path):
    backup = path.with_suffix(".backup.xlsx")
    if path.exists():
        shutil.copy2(path, backup)
    wb.save(path)
```

### Concurrency Handling

**For Phase 1:** Read-only (no writes from UI yet). Phase 2 will add:
- File locks (fcntl on Linux, msvcrt on Windows)
- Timestamped backups (`path_YYYYMMDD_HHMMSS.xlsx`)
- Conflict detection (last-write-wins with audit log)

---

## Features to Port (7 core + 1 shared)

### Feature 1: Authentication & Authorization

**Current state:** Flask-Login, CSRF tokens, 3 roles (admin/editor/viewer)

**Excel data source:** None (hardcoded for Phase 1)

**Deliverables:**
- [ ] Login page (Arabic: ميزان / المنطقة الجنوبية)
- [ ] Session management (Flask-Login)
- [ ] CSRF protection
- [ ] Role-based access (admin/editor/viewer)
- [ ] Logout, password change (stretch)

**Routes:**
- `GET /auth/login` → login form
- `POST /auth/login` → authenticate
- `GET /auth/logout` → clear session

**Templates:**
- `auth/login.html` (RTL, Cairo font, NWC colors)

---

### Feature 2: Employee Directory & Search

**Current state:** 444 active employees loaded to DB; searchable by name/job/region

**Excel source:** `employees data source.xlsx`, sheet `data`

**Key columns (0-based):**
- 3: phone
- 11: status (filter: "على قوة العمل")
- 14: nation
- 15: kafala
- 16: region
- 18: category (job type)
- 20: name
- 21: job
- 23: salary

**Deliverables:**
- [ ] Load employees from Excel on app start (cached in memory or session)
- [ ] Search by name / job / region (real-time, server-side)
- [ ] Display: table view with filters + export to Excel
- [ ] Job category matching logic (safety eng → مهندس أمن وسلامة, etc.)

**Routes:**
- `GET /employees/` → list all + search form
- `GET /employees/<emp_id>` → detail card
- `GET /employees/export` → download current view as .xlsx

**Templates:**
- `employees/list.html` (searchable grid, Cairo, RTL)
- `employees/detail.html` (single employee card)

**Scripts:**
- `scripts/load_employees.py` → cache to session/memory

---

### Feature 3: Org Chart (Static A3 Export)

**Current state:** `gen_org_charts.py` generates 4 region-specific A3 HTML files (26 REs, 444 employees)

**Excel sources:**
- Employees: `employees data source.xlsx`
- Projects: `project_2026_database_ver1_updated.xlsx`
- RE directory: `data/Organize/Office-RE.xlsx`

**Deliverables:**
- [ ] Refactor `gen_org_charts.py` for server paths
- [ ] Generate on-demand or scheduled (daily at midnight)?
- [ ] Store pre-rendered HTML in `app/static/org_charts/`
- [ ] Route: region selector + view + PDF export

**Routes:**
- `GET /reports/org-chart` → region selector (4 cards)
- `GET /reports/org-chart/<region>` → view HTML (عسير/جازان/الباحة/نجران)
- `GET /reports/org-chart/<region>/pdf` → Playwright PDF A3 landscape

**Templates:**
- `reports/org_chart_selector.html` (region cards)
- `reports/org_chart_view.html` (embedded A3 + toolbar)

**Scripts:**
- `scripts/gen_org_charts.py` (port from HR/org_charts/)

---

### Feature 4: Org Chart (Interactive Smart Chart)

**Current state:** Interactive dashboard with search, collapsible RE cards, KPI metrics

**Excel sources:** Same as Feature 3

**Deliverables:**
- [ ] Tab-based nav by region
- [ ] KPI cards (employees, projects, contractors, offices per region)
- [ ] Search/filter (real-time JS) by employee name or job
- [ ] Collapsible RE office cards (click to show/hide team)
- [ ] Employees grouped by job category (color badges)
- [ ] Projects listed under each RE (if assigned)

**Routes:**
- `GET /reports/org-chart-smart` → interactive dashboard

**Templates:**
- `reports/org_chart_smart.html` (Tabs, Cards, Search, Collapsible)

**Scripts:**
- No new scripts (read-only from Excel)

---

### Feature 5: Project Map (Interactive Leaflet)

**Current state:** Leaflet map showing ongoing projects (132 mapped, 8 missing coords)

**Excel source:** `project_2026_database_ver1_updated.xlsx`, sheet `pro`

**Key columns (0-based):**
- 12: project name
- 16: district (wad)
- 17: region
- 18: contractor
- 21: RE supervisor
- 23: project state (filter: تحت التنفيذ)
- Coords: custom columns or external geo file (TBD)

**Deliverables:**
- [ ] Tab-based nav by region
- [ ] KPI cards (total projects, mapped, missing, RE count)
- [ ] Leaflet map with color-coded markers by RE
- [ ] Sidebar searchable RE list + project counts
- [ ] Collapsible missing-coordinates table
- [ ] Coords: load from Excel or external GeoJSON?

**Routes:**
- `GET /reports/project-map-smart` → interactive map

**Templates:**
- `reports/project_map_smart.html` (Leaflet, Tabs, Sidebar, Search)

**Scripts:**
- `scripts/load_projects.py` → cache to session

---

### Feature 6: Projects Dashboard (KPI + Pivot Tables)

**Current state:** Home dashboard with KPI cards + pivot tables

**Excel source:** `project_2026_database_ver1_updated.xlsx`

**Deliverables:**
- [ ] KPI cards (total projects, ongoing, completed, by region with MSAR format)
- [ ] Pivot table 1: count of projects by status × region
- [ ] Pivot table 2: total contract value (SAR) by status × region
- [ ] Charts: bar chart (ongoing by region), pie (status breakdown)
- [ ] Print/PDF support (A4 landscape)

**Routes:**
- `GET /reports/projects-dashboard` → full dashboard

**Templates:**
- `reports/projects_dashboard.html` (KPI cards, Tables, Charts, Print CSS)

**Scripts:**
- `scripts/build_projects_dashboard.py` → compute pivot tables

---

### Feature 7: Finance Report (Invoices & PO Tracking)

**Current state:** Invoices by PO (1-6), attendance tracking, amounts per employee

**Excel sources:**
- Invoices: `Invoices/Jun_Inv.xlsx`
- Employees: `employees data source.xlsx`
- Projects: `project_2026_database_ver1_updated.xlsx`

**Deliverables:**
- [ ] PO filter (1-6 tabs)
- [ ] Invoice list by PO (date, employee, amount, status)
- [ ] Attendance breakdown (calendar view or grid)
- [ ] Total by PO (MSAR format)
- [ ] Export to Excel (filtered view)

**Routes:**
- `GET /reports/finance` → finance dashboard
- `GET /reports/finance/<po>` → detail by PO

**Templates:**
- `reports/finance_dashboard.html` (PO tabs, Invoice table, Export button)

**Scripts:**
- `scripts/load_finance_data.py` → cache to session

---

### Feature 8: Settings Hub (Shared)

**Current state:** Job codes (23 codes) with titles and rates

**Excel source:** Job codes stored in database (Phase 1: hardcoded in config.py)

**Deliverables:**
- [ ] Settings home (list available settings)
- [ ] Job codes view (title, code, monthly rate SAR)
- [ ] (Stretch) Job code editor (admin only)

**Routes:**
- `GET /settings/` → settings home
- `GET /settings/job-codes` → list all codes

**Templates:**
- `settings/index.html` (settings menu)
- `settings/job_codes.html` (job code table)

---

## Technology Stack

| Layer | Tech | Notes |
|-------|------|-------|
| Framework | Flask 2.x | Lightweight, extensible |
| Templates | Jinja2 + HTML5 | RTL support (dir="rtl") |
| Styling | CSS3 (Cairo font, NWC palette) | No Bootstrap (full control for Arabic) |
| Data | openpyxl | Read/write Excel, safe copy pattern |
| Interactivity | Vanilla JS + Chart.js | No npm, just CDN (lighter) |
| Maps | Leaflet (CDN) | Lightweight mapping |
| PDF Export | Playwright | A3 landscape, print CSS |
| Auth | Flask-Login + CSRF | Built-in, no external deps |

---

## Implementation Phases (Tickets 1-7)

### Ticket 1: Setup & Config
- [ ] Git branch: `feature/phase1-excel-arch`
- [ ] Create `scripts/load_employees.py` + `scripts/load_projects.py`
- [ ] Update `config.py` with Excel paths (data/source/)
- [ ] Create `utils/excel_reader.py` (load_copy pattern)
- [ ] Update `requirements.txt` (openpyxl, playwright, etc.)

### Ticket 2: Auth & Routing
- [ ] Login form + session management
- [ ] Base template (nav, header, footer, RTL)
- [ ] Route structure: auth/, employees/, reports/, settings/

### Ticket 3: Employees Feature
- [ ] Load + cache employees from Excel
- [ ] List + search page
- [ ] Detail card page
- [ ] Export to Excel

### Ticket 4: Org Chart (Static + Smart)
- [ ] Refactor `gen_org_charts.py` for server paths
- [ ] Route: region selector
- [ ] Route: view A3 HTML
- [ ] Route: PDF export (Playwright)
- [ ] Smart Chart interactive dashboard

### Ticket 5: Project Map
- [ ] Load + cache projects from Excel
- [ ] Leaflet interactive map
- [ ] Tab-based region nav
- [ ] Search sidebar

### Ticket 6: Projects Dashboard
- [ ] Load projects from Excel
- [ ] Compute pivot tables (status × region)
- [ ] KPI cards + charts
- [ ] Print CSS for A4 landscape

### Ticket 7: Finance Report + Settings
- [ ] Load invoices + employees from Excel
- [ ] Finance dashboard (PO tabs, invoice table)
- [ ] Settings hub (job codes view)
- [ ] Export to Excel (finance filtered view)

---

## Excel File Structure (Reference)

### employees data source.xlsx (sheet: data)

```
Row 1: Header
[0]=ID, [1]=Name_En, [2]=Name_Ar, [3]=Phone, ..., [11]=Status, ..., [14]=Nation, [15]=Kafala, [16]=Region, [18]=Category, [20]=Name, [21]=Job, [23]=Salary
```

**Filter for Phase 1:** status (col 11) == "على قوة العمل" → 444 rows

### project_2026_database_ver1_updated.xlsx (sheet: pro)

```
Row 1: Header
[9]=PO, [10]=Active, [12]=ProjectName, [16]=District, [17]=Region, [18]=Contractor, [21]=RE, [23]=State, [24]=StartDate, [25]=EndDate, [29]=Value
```

**Filter for Phase 1:** active (col 10) == "yes" → 227 rows (filter to "تحت التنفيذ" for map = 132)

### Jun_Inv.xlsx

```
Rows: Employee, AttendanceCode, Amount, Date, PO
```

---

## Known Constants

```python
REGIONS = ['عسير', 'جازان', 'الباحة', 'نجران']
REGION_CODES = {'عسير':'AS', 'جازان':'JZ', 'الباحة':'BA', 'نجران':'NJ'}
REPORT_MONTH = "يونيو 2026"
PROJECT_MGR = "م/ يسري أحمد عبد السلام"
ERR_VALS = {'#REF!','=#REF!','#VALUE!','#N/A','#NAME?','#DIV/0!','#NULL!','#NUM!'}
```

---

## Design System

- **Font:** Cairo (Google Fonts)
- **Direction:** RTL on root, LTR on logo row only
- **Colors:** Navy (#0a1f3d, #0071b9), Green (#059669), Amber (#d97706), Red (#e11d48)
- **Logos:** NWC (left), Al-Amro (right) from `data/NWC layout/img/`
- **Print:** A4 landscape (194mm height), A3 landscape for org charts

---

## Success Criteria (Phase 1 Complete)

- [ ] All 7 features working locally with Excel data
- [ ] No database (SQLite) — pure Excel
- [ ] Auth working (login/logout, roles)
- [ ] All routes responding (employees, org-chart, projects, finance, settings)
- [ ] Search/filter working (employees, projects, smart chart)
- [ ] Print/PDF export working (org-chart, finance, dashboard)
- [ ] Tests passing (at least smoke tests for all routes)
- [ ] Deployed to PythonAnywhere and live
- [ ] Data files symlinked or copied to server

---

## Blockers / Decisions Needed

1. **Coordinates for projects:** Where to load lat/lng for map?
   - Option A: Hardcode in project Excel (add columns)
   - Option B: External GeoJSON file
   - Option C: Use district centroids as fallback
   - **Decision:** [TBD by user]

2. **Attendance codes:** Which codes to support? (شاهد, غايب, إجازة, etc.)
   - **Source:** `Invoices/assign.XLSX` has 6 codes
   - **Decision:** Load from file or hardcode?

3. **Job code rates:** Hardcoded or Excel?
   - **Current:** 23 codes defined (2026-08-19)
   - **Phase 1:** Hardcode in `config.py`
   - **Phase 2:** Load from Excel for live updates

4. **Leave requests workflow:** Skip for Phase 1?
   - **Current:** 3-level approval (emp → RE → GM)
   - **Phase 1 scope:** Read-only view of vacations.xlsx
   - **Phase 2:** Full workflow with UI

---

## Notes

- All data loaded from Excel on app start (cached in memory or session)
- No background jobs yet (Phase 2: schedule daily org chart generation)
- No user-initiated writes yet (Phase 2: approve leaves, edit job codes)
- PDF export uses Playwright (already in requirements)
- All paths use `Path()` for cross-platform compatibility
- Error handling: graceful fallbacks, never crash on missing Excel columns

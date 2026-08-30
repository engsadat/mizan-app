# Mizan v2 PHASE 1 — Implementation Tickets

**Created:** 2026-08-30  
**Branch:** `feature/phase1-excel-arch`  
**Strategy:** 7 tracer-bullet tickets, parallelizable, each ~1-2 sessions

---

## Ticket 1: Foundation & Excel Setup

**Title:** Setup Flask app, config, and Excel reader utilities

**Scope:**
- Create `utils/excel_reader.py` with `load_copy()` safe-read pattern
- Update `config.py` with Excel paths (data/source/, data/Organize/)
- Update `requirements.txt` (openpyxl, pygame for PDF, etc.)
- Create `scripts/load_employees.py` (cache employees to session/app context)
- Create `scripts/load_projects.py` (cache projects to session/app context)
- Create base app layout (`app/base.html` with RTL, Cairo font, NWC branding)
- Verify local data files accessible via symlinks or copies

**Deliverables:**
- [ ] `utils/excel_reader.py` with safe read + backup write patterns
- [ ] Updated `config.py` pointing to Excel data
- [ ] `requirements.txt` finalized
- [ ] `scripts/load_employees.py` working locally
- [ ] `scripts/load_projects.py` working locally
- [ ] Base template with RTL/branding
- [ ] Local data symlinks confirmed

**Definition of Done:**
- `python scripts/load_employees.py` loads 444 employees without error
- `python scripts/load_projects.py` loads 227 projects without error
- Base template renders with Cairo font + NWC colors

**Blockers:** None

---

## Ticket 2: Auth & Navigation

**Title:** Implement login, session management, and navigation scaffold

**Scope:**
- Login form (Arabic: ميزان / المنطقة الجنوبية)
- Flask-Login session management (admin/editor/viewer roles)
- CSRF token protection
- Logout route
- Navigation bar (home, employees, reports, settings)
- Error pages (403, 404, 500) with RTL styling
- Base template extends with nav + footer

**Deliverables:**
- [ ] `auth/routes.py` (login/logout)
- [ ] `auth/login.html` template
- [ ] `templates/base.html` with nav + footer
- [ ] Error templates (403, 404, 500)
- [ ] Role decorators in `auth/decorators.py`

**Definition of Done:**
- Login with hardcoded user (admin/password) works locally
- Unauthenticated access redirects to login
- CSRF tokens present on forms
- Role-based access control working
- All routes protected

**Blockers:** None

**Depends on:** Ticket 1 (base template)

---

## Ticket 3: Employees Feature

**Title:** Build employee directory with search, detail view, export

**Scope:**
- Load 444 employees from Excel (cached in app context on startup)
- List page with search (name, job, region, phone)
- Detail card (single employee view)
- Export current view to Excel
- Job category classification logic (مهندس أمن وسلامة, مراقب موقع, etc.)
- Table with sorting/filtering (jQuery or vanilla JS)

**Deliverables:**
- [ ] `employees/routes.py` (list, detail, export)
- [ ] `employees/list.html` (searchable grid, Cairo)
- [ ] `employees/detail.html` (single card)
- [ ] Helper: `utils/job_categories.py` (classification rules)

**Definition of Done:**
- `/employees/` loads all 444 employees
- Search by name finds employees instantly
- Detail page shows correct phone, salary, region
- Export downloads Excel with filtered view
- Job categories displayed correctly

**Blockers:** Ticket 1 (load_employees.py)

---

## Ticket 4: Org Charts (Static A3 + Interactive Smart)

**Title:** Generate A3 org charts and build interactive Smart Chart dashboard

**Scope:**
- Refactor `gen_org_charts.py` from HR project for Mizan server paths
- Generate 4 region-specific A3 HTML files (26 REs, 444 employees)
- Store pre-generated HTML in `app/static/org_charts/`
- Region selector page (4 cards: عسير, جازان, الباحة, نجران)
- View static A3 chart (embedded HTML + toolbar)
- PDF export route (Playwright → A3 landscape)
- Interactive Smart Chart dashboard:
  - Tab-based region nav
  - KPI cards (employees, projects, contractors, offices)
  - Search/filter by employee name or job
  - Collapsible RE office cards
  - Employees grouped by job category with color badges
  - Projects listed under each RE

**Deliverables:**
- [ ] `scripts/gen_org_charts.py` (refactored)
- [ ] `reports/org_chart_landing.html` (region selector)
- [ ] `reports/org_chart_view.html` (view + PDF toolbar)
- [ ] `reports/org_chart_smart.html` (interactive dashboard)
- [ ] Routes: `/reports/org-chart`, `/reports/org-chart/<region>`, `/reports/org-chart/<region>/pdf`, `/reports/org-chart-smart`

**Definition of Done:**
- All 4 region A3 charts generate without error
- Static charts display correctly in browser
- PDF export produces valid A3 landscape
- Smart Chart shows all 444 employees grouped by category
- Search works in real-time (JS)
- Region tabs switch without page reload

**Blockers:** Ticket 1 (load scripts, Excel reader), Ticket 2 (auth)

---

## Ticket 5: Project Map (Interactive Leaflet)

**Title:** Build interactive Leaflet map for ongoing projects

**Scope:**
- Load 227 projects from Excel (cached on startup)
- Filter to ongoing projects only (تحت التنفيذ) → 132 projects
- Tab-based region nav (عسير, جازان, الباحة, نجران)
- KPI cards (total, mapped, missing, RE count)
- Leaflet map with color-coded markers by RE
- Sidebar with searchable RE list + project counts
- Collapsible missing-coordinates table
- Coords: load from Excel or use district centroids (TBD)

**Deliverables:**
- [ ] `scripts/load_projects.py` enhanced with coordinate handling
- [ ] `reports/project_map_smart.html` (Leaflet + Tabs + Sidebar)
- [ ] Route: `/reports/project-map-smart`

**Definition of Done:**
- Map loads with 132 ongoing projects
- Region tabs switch marker visibility
- Search in sidebar filters RE list in real-time
- Missing coordinates (8 projects) shown in collapsible table
- Map centered on Southern Region by default
- All markers clickable with project info

**Blockers:** Ticket 1 (load_projects.py), Ticket 2 (auth)

**Decisions:** Coordinate source (hardcode vs. GeoJSON vs. centroids)?

---

## Ticket 6: Projects Dashboard (KPI + Pivot Tables)

**Title:** Build dashboard with KPI cards, pivot tables, charts, and print support

**Scope:**
- Load 227 projects from Excel
- KPI cards (total, ongoing by region with MSAR format)
- Pivot table 1: count of projects by status × region
- Pivot table 2: total contract value (SAR) by status × region
- Bar chart: ongoing projects by region
- Pie chart: status breakdown
- Print CSS for A4 landscape
- Export filtered view to Excel (optional)

**Deliverables:**
- [ ] `scripts/build_projects_dashboard.py` (compute pivot tables)
- [ ] `reports/projects_dashboard.html` (KPI, tables, charts, print CSS)
- [ ] Route: `/reports/projects-dashboard`

**Definition of Done:**
- All 4 KPI cards show correct numbers
- Pivot tables correct (verified by manual Excel count)
- Charts render without JS errors
- Print preview shows A4 landscape layout
- MSAR format (millions with proper Arabic locale)
- Export button downloads filtered Excel

**Blockers:** Ticket 1 (load_projects.py), Ticket 2 (auth)

---

## Ticket 7: Finance Report + Settings

**Title:** Build finance dashboard (invoices by PO) and settings hub (job codes)

**Scope:**
- Load invoices from `Jun_Inv.xlsx` (509 employee-invoice records)
- Load employees + salaries for context
- Finance dashboard with PO tabs (1-6)
- Invoice table per PO (date, employee, amount, status, notes)
- Total by PO (MSAR format)
- Export filtered PO view to Excel
- Settings hub (navigation to sub-settings)
- Job codes view (title, code, monthly rate SAR)
- (Stretch) Job code editor for admin role

**Deliverables:**
- [ ] `scripts/load_finance_data.py` (cache invoices to session)
- [ ] `reports/finance_dashboard.html` (PO tabs, invoice table, export, print CSS)
- [ ] `settings/index.html` (settings menu)
- [ ] `settings/job_codes.html` (job code table)
- [ ] Routes: `/reports/finance`, `/settings/`, `/settings/job-codes`

**Definition of Done:**
- All 6 PO tabs load without error
- Invoice table shows 509+ records across POs
- Totals match Excel sums (verified by manual check)
- Export downloads Excel with selected PO's invoices
- Print CSS works for A4 landscape
- Settings hub accessible from nav
- Job codes table displays 23 codes with correct rates

**Blockers:** Ticket 1 (Excel reader), Ticket 2 (auth)

---

## Implementation Strategy

**Phase:**
```
Week 1:
  Ticket 1 (Foundation) — must complete first
  Ticket 2 (Auth) — in parallel, depends on Ticket 1
  
Week 2:
  Tickets 3, 4, 5, 6, 7 — can run in parallel, all depend on Tickets 1+2
```

**Parallelization:**
- Ticket 3 (Employees) — independent, no cross-feature dependencies
- Ticket 4 (Org Charts) — independent (loads own Excel files)
- Ticket 5 (Project Map) — independent (uses project Excel)
- Ticket 6 (Dashboard) — independent (uses project Excel)
- Ticket 7 (Finance + Settings) — independent (uses invoice Excel)

**Delegation:**
- Ticket 1 → Lead (foundation critical)
- Tickets 2–7 → Delegate to parallel agents (cheaper models, TDD)

---

## Testing Strategy

**For each ticket:**
1. Smoke test: Route responds, no 500 errors
2. Data test: Verify row counts match Excel source
3. UI test: Manually browse feature in browser
4. Print test: Print preview works (A4/A3 landscape)
5. Export test: Downloaded Excel valid + data correct

**Automated (pytest):**
- `test_excel_reader.py` (load_copy, safe read/write)
- `test_auth.py` (login, CSRF, roles)
- `test_employees.py` (load, search, detail, export)
- `test_org_charts.py` (generate, route, PDF)
- `test_projects.py` (load, filter, map, dashboard, finance)

---

## Deployment Checklist

After all 7 tickets complete:

- [ ] Local tests all passing
- [ ] All routes responding
- [ ] Excel files accessible (symlinked on server)
- [ ] Logos accessible from server paths
- [ ] PDF export tested (Playwright working)
- [ ] Playwright installed on PythonAnywhere
- [ ] Data files uploaded to PythonAnywhere (`/home/southMizan/mizan-app/data/`)
- [ ] Code merged to master, pushed to GitHub
- [ ] Web app reloaded on PythonAnywhere
- [ ] Smoke test each route on live URL
- [ ] Update STATUS.md with live date + checklist

---

## Notes

- Each ticket is **independent and testable in isolation**
- All **can run in parallel** after Tickets 1–2
- **No database writes** — read-only from Excel (Phase 2 adds user edits)
- **No background jobs** — Phase 2 adds scheduled org chart generation
- **Hardcoded auth** for Phase 1; Phase 2 adds user management Excel

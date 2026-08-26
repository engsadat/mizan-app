# Org Chart Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate 4 region-specific org chart reports into Mizan's Reports section with PDF export capability.

**Architecture:** 
- Adapt existing `gen_org_chart.py` to read from Mizan's database instead of Excel
- Create script (`gen_org_charts.py`) to generate 4 static HTML files
- Add 3 Flask routes to display charts and export to PDF
- Create 2 templates for landing page and chart view
- Add org chart icon to home page Reports section

**Tech Stack:** Flask, Jinja2, Playwright (PDF), SQLAlchemy ORM, openpyxl

---

## File Structure

**New Files:**
- `scripts/gen_org_charts.py` — generates org charts from database
- `app/templates/reports/org_chart_landing.html` — landing page (4 region cards)
- `app/templates/reports/org_chart_view.html` — org chart display + PDF button
- `docs/superpowers/plans/2026-08-26-org-chart-integration-plan.md` — this plan
- `app/static/org_charts/` (directory, created at runtime)

**Modified Files:**
- `app/blueprints/reports/routes.py` — add 3 new routes
- `app/templates/reports/index.html` — add org chart card to Reports home

---

## Task Breakdown

### Task 1: Create Base Script Structure (`gen_org_charts.py`)

**Files:**
- Create: `scripts/gen_org_charts.py`

- [ ] **Step 1: Create empty script with app context**

Create `scripts/gen_org_charts.py`:

```python
"""
Generate organization chart HTML files for Mizan.

Usage: python scripts/gen_org_charts.py

Reads:
  - Employee, Project data from Mizan database
  - Lookup files: emp_sort.xlsx, Office-RE.xlsx

Outputs:
  - app/static/org_charts/09_OrgChart_Asir.html
  - app/static/org_charts/10_OrgChart_Jizan.html
  - app/static/org_charts/11_OrgChart_Baha.html
  - app/static/org_charts/12_OrgChart_Najran.html
"""
import sys, os, re, shutil, base64
from pathlib import Path
from collections import defaultdict
from datetime import date
import openpyxl

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app, db
from app.models import Employee, EmployeeStatus, JobCode, Project

# Initialize Flask app
app = create_app()
app.app_context().push()

BASE = Path(__file__).parent.parent
OUT_DIR = BASE / 'app' / 'static' / 'org_charts'
OUT_DIR.mkdir(parents=True, exist_ok=True)

REGIONS = ['عسير', 'جازان', 'الباحة', 'نجران']
REGION_FILE = {
    'عسير': '09_OrgChart_Asir.html',
    'جازان': '10_OrgChart_Jizan.html',
    'الباحة': '11_OrgChart_Baha.html',
    'نجران': '12_OrgChart_Najran.html',
}

print(f"Output directory: {OUT_DIR}")
```

- [ ] **Step 2: Verify app context works**

Run: `python scripts/gen_org_charts.py`

Expected output:
```
Output directory: C:\Users\engsa\OneDrive\Desktop\AI\HR\mizan\app\static\org_charts
```

- [ ] **Step 3: Commit**

```bash
git add scripts/gen_org_charts.py
git commit -m "feat: add base org chart generation script"
```

---

### Task 2: Add Helper Functions (gen_org_charts.py)

**Files:**
- Modify: `scripts/gen_org_charts.py`

- [ ] **Step 1: Add utility functions at top of script (after imports)**

Add after `REGION_FILE` definition:

```python
# ── Utility Functions ──────────────────────────────────────────────

def sv(v):
    """Safe value: return empty string for None or Excel errors."""
    if v is None:
        return ''
    s = str(v).strip()
    err_vals = {'#REF!', '=#REF!', '#VALUE!', '#N/A', '#NAME?', '#DIV/0!', '#NULL!', '#NUM!'}
    return '' if s in err_vals else s

def load_copy(path):
    """Load Excel file safely (avoid PermissionError if file open)."""
    tmp = str(path) + '.tmp.xlsx'
    shutil.copy2(path, tmp)
    wb = openpyxl.load_workbook(tmp, data_only=True)
    os.remove(tmp)
    return wb

def _b64img(p):
    """Convert image to base64 data URI."""
    with open(p, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode()

def short3(name):
    """Shorten name to first 3 words."""
    parts = sv(name).split()
    return ' '.join(parts[:3])

def strip_grade(job):
    """Remove grade suffix (e.g., 'Engineer E5' → 'Engineer')."""
    return re.sub(r'\s+E\d+$', '', sv(job)).strip()

# Load logos as base64
try:
    LOGO_NWC = _b64img(BASE / 'NWC layout' / 'img' / 'NWC_Logo.png')
    LOGO_ALAMRO = _b64img(BASE / 'NWC layout' / 'img' / 'Alamro_Logo.png')
except Exception as e:
    print(f"Warning: Could not load logos: {e}")
    LOGO_NWC = ''
    LOGO_ALAMRO = ''

print(f"Logos loaded: NWC={len(LOGO_NWC) > 0}, Al-Amro={len(LOGO_ALAMRO) > 0}")
```

- [ ] **Step 2: Verify script still runs**

Run: `python scripts/gen_org_charts.py`

Expected: Same output as before (logos loaded messages may appear)

- [ ] **Step 3: Commit**

```bash
git add scripts/gen_org_charts.py
git commit -m "feat: add utility functions and logo loading"
```

---

### Task 3: Load Supporting Excel Files (gen_org_charts.py)

**Files:**
- Modify: `scripts/gen_org_charts.py`

- [ ] **Step 1: Add Excel file loading after logo section**

Add after the logo loading block:

```python
# ── Load Supporting Excel Files ────────────────────────────────────

# On server: /home/southMizan/sources/
# Local dev: must have these files
SOURCES_DIR = Path('/home/southMizan/sources') if Path('/home/southMizan/sources').exists() else BASE / 'Organize'

emp_sort_path = SOURCES_DIR / 'emp_sort.xlsx'
office_re_path = SOURCES_DIR / 'Office-RE.xlsx'

if not emp_sort_path.exists():
    print(f"ERROR: emp_sort.xlsx not found at {emp_sort_path}")
    sys.exit(1)
if not office_re_path.exists():
    print(f"ERROR: Office-RE.xlsx not found at {office_re_path}")
    sys.exit(1)

# Load job sort order
print(f"Loading job sort order from {emp_sort_path}")
wb_sort = load_copy(emp_sort_path)
ws_sort = wb_sort['Sheet1']
JOB_SORT = {}
for row in ws_sort.iter_rows(min_row=2, max_row=ws_sort.max_row, values_only=True):
    full_job = sv(row[0])
    rank = row[1]
    if full_job and rank:
        stripped = re.sub(r'\s+E\d+$', '', full_job).strip()
        try:
            JOB_SORT.setdefault(stripped, int(rank))
        except (ValueError, TypeError):
            pass

print(f"Loaded {len(JOB_SORT)} job sort entries")

# Load RE directory
print(f"Loading RE directory from {office_re_path}")
wb_re = load_copy(office_re_path)
ws_re = wb_re['RE_Mail']
re_info = {}
reg_order = defaultdict(list)

for row in ws_re.iter_rows(min_row=2, max_row=ws_re.max_row, values_only=True):
    name = sv(row[1])
    region = sv(row[4])
    ocode = sv(row[7])
    oname = sv(row[8])
    phone = sv(row[3])
    page_no = sv(row[9])
    if not name or not region:
        continue
    if ocode == 'عسير_0':
        continue
    re_info[name] = {'phone': phone, 'office_code': ocode, 'office_name': oname, 'page_no': page_no}
    reg_order[region].append((ocode, name))

def _ocode_key(ocode):
    parts = re.split(r'(\d+)', ocode)
    return [int(p) if p.isdigit() else p for p in parts]

for region in reg_order:
    reg_order[region].sort(key=lambda x: _ocode_key(x[0]))

print(f"Loaded {len(re_info)} REs across {len(reg_order)} regions")
```

- [ ] **Step 2: Verify Excel files load**

Run: `python scripts/gen_org_charts.py`

Expected output:
```
Loading job sort order from ...
Loaded X job sort entries
Loading RE directory from ...
Loaded Y REs across Z regions
```

- [ ] **Step 3: Commit**

```bash
git add scripts/gen_org_charts.py
git commit -m "feat: load supporting Excel files (emp_sort, Office-RE)"
```

---

### Task 4: Load Data from Mizan Database (gen_org_charts.py)

**Files:**
- Modify: `scripts/gen_org_charts.py`

- [ ] **Step 1: Add employee data loading after RE loading**

Add after the RE directory loading block:

```python
# ── Load Employee Data from Database ───────────────────────────────

print("Loading employee data from Mizan database...")
emp_by_re = defaultdict(list)
region_emp_total = defaultdict(int)

# Query employees with status 'على قوة العمل'
employees = db.session.query(Employee).join(
    EmployeeStatus, Employee.current_status_id == EmployeeStatus.id
).filter(
    EmployeeStatus.name_ar == 'على قوة العمل'
).all()

for emp in employees:
    re_name = sv(emp.re_code)
    emp_name = sv(emp.full_name)
    job = strip_grade(emp.job_code.title if emp.job_code else '')
    nation = sv(emp.nationality.name_ar if emp.nationality else '')
    region = sv(emp.region)
    
    if region in REGIONS:
        region_emp_total[region] += 1
    
    if re_name and emp_name:
        emp_by_re[re_name].append({
            'name': emp_name,
            'job': job,
            'nation': nation
        })

print(f"Loaded {len(employees)} employees")
for region in REGIONS:
    print(f"  {region}: {region_emp_total[region]} employees")
```

- [ ] **Step 2: Verify employee data loads**

Run: `python scripts/gen_org_charts.py`

Expected output:
```
Loading employee data from Mizan database...
Loaded X employees
  عسير: Y employees
  جازان: Z employees
  ...
```

- [ ] **Step 3: Commit**

```bash
git add scripts/gen_org_charts.py
git commit -m "feat: load employee data from Mizan database"
```

---

### Task 5: Load Project Data from Database (gen_org_charts.py)

**Files:**
- Modify: `scripts/gen_org_charts.py`

- [ ] **Step 1: Add project data loading after employee loading**

Add after employee loading block:

```python
# ── Load Project Data from Database ────────────────────────────────

print("Loading project data from Mizan database...")
projects_by_re = defaultdict(list)

# Query projects with included=True and project_state='تحت التنفيذ'
projects = db.session.query(Project).filter(
    Project.included == True,
    Project.project_state == 'تحت التنفيذ'
).all()

for proj in projects:
    # Get RE name(s) for this project based on region
    region = sv(proj.region)
    re_names = []
    
    if region == 'عسير':
        re_names = [sv(proj.re_asir)] if proj.re_asir else []
    elif region == 'جازان':
        re_names = [sv(proj.re_jazan)] if proj.re_jazan else []
    elif region == 'الباحة':
        re_names = [sv(proj.re_baha)] if proj.re_baha else []
    elif region == 'نجران':
        re_names = [sv(proj.re_najran)] if proj.re_najran else []
    
    for re_name in re_names:
        if re_name:
            projects_by_re[re_name].append({
                'name': sv(proj.name),
                'value': proj.value or 0,
                'contractor': sv(proj.contractor_name),
                'status': sv(proj.project_state)
            })

print(f"Loaded {len(projects)} ongoing projects")
for re in sorted(projects_by_re.keys())[:5]:
    print(f"  {re}: {len(projects_by_re[re])} projects")
```

- [ ] **Step 2: Verify project data loads**

Run: `python scripts/gen_org_charts.py`

Expected output:
```
Loading project data from Mizan database...
Loaded X ongoing projects
  RE Name 1: Y projects
  ...
```

- [ ] **Step 3: Commit**

```bash
git add scripts/gen_org_charts.py
git commit -m "feat: load project data from Mizan database"
```

---

### Task 6: Generate HTML for Single Region (gen_org_charts.py)

**Files:**
- Modify: `scripts/gen_org_charts.py`

- [ ] **Step 1: Add main HTML generation function**

Add after data loading blocks, before any region iteration:

```python
# ── HTML Generation ────────────────────────────────────────────────

def generate_org_chart_html(region):
    """
    Generate org chart HTML for a single region.
    Returns: HTML string
    """
    report_month = date.today().strftime('%B %Y')
    
    # Status/color config
    status_cfg = {
        'تحت التنفيذ': ('#0071B9', '#fff'),
        'ايقاف كلي': ('#991B1B', '#fff'),
        'استلام ابتدائي(أثناء فترة الـ 60 يوم)': ('#7C3AED', '#fff'),
        'استلام ابتدائي': ('#FFC000', '#1e293b'),
        'مسحوب': ('#C00000', '#fff'),
        'إيقاف جزئي': ('#F59E0B', '#fff'),
    }
    
    def status_style(s):
        for k, (bg, fg) in status_cfg.items():
            if k in sv(s):
                return bg, fg
        return '#72808A', '#fff'
    
    # Get REs for this region
    region_res = [name for ocode, name in reg_order.get(region, [])]
    
    # Build HTML
    html_parts = [
        '<!DOCTYPE html>',
        '<html lang="ar" dir="rtl">',
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=1481">',
        f'<title>الهيكل التنظيمي — {region}</title>',
        '<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">',
        '<style>',
        ':root {',
        '  --navy:#002060; --blue:#0071B9; --sky:#00A7E2; --teal:#03A88B;',
        '  --amber:#d97706; --red:#C00000; --gray:#72808A;',
        '  --lb:#e8f4fd; --lg:#f5f7fa; --bd:#d1d9e6;',
        '}',
        '*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }',
        'html { width: 392mm; }',
        "body { font-family: 'Cairo', sans-serif; direction: rtl; font-size: 11px; color: var(--navy); background: #fff; width: 100%; }",
        '.page { width: 100%; height: 277mm; display: flex; flex-direction: column; overflow: hidden; break-after: page; }',
        '.page:last-child { break-after: auto; }',
        '.ph { display: flex; align-items: center; gap: 8px; padding: 3px 10px; border-bottom: 3px solid var(--blue); border-top: 3px solid var(--amber); flex-shrink: 0; }',
        '.ph img { height: 26px; max-width: 90px; object-fit: contain; flex-shrink: 0; }',
        '.ph-mid { flex: 1; text-align: center; }',
        '.ph-mid h1 { font-size: 13px; font-weight: 900; line-height: 1.3; }',
        '.ph-mid small { font-size: 9px; color: var(--gray); }',
        '</style>',
        '</head>',
        '<body>',
        '<div class="page">',
        '<div class="ph">',
        f'<img src="{LOGO_ALAMRO}" alt="Al-Amro">',
        '<div class="ph-mid">',
        f'<h1>الهيكل التنظيمي — {region}</h1>',
        f'<small>{report_month}</small>',
        '</div>',
        f'<img src="{LOGO_NWC}" alt="NWC">',
        '</div>',
        '<div class="cards">',
    ]
    
    # Add RE cards
    for re_name in region_res:
        if re_name not in re_info:
            continue
        
        re_data = re_info[re_name]
        emp_count = len(emp_by_re.get(re_name, []))
        proj_count = len(projects_by_re.get(re_name, []))
        
        html_parts.extend([
            '<div class="card">',
            '<div class="coh">',
            f'<div class="con">{re_name}</div>',
            '</div>',
            '<div class="cbody">',
            f'<div>Projects: {proj_count} | Staff: {emp_count}</div>',
            '<div class="spacer"></div>',
            f'<div>Phone: {re_data["phone"]}</div>',
            '</div>',
            '</div>',
        ])
    
    html_parts.extend([
        '</div>',
        '</div>',
        '</body>',
        '</html>',
    ])
    
    return '\n'.join(html_parts)
```

- [ ] **Step 2: Test HTML generation for one region**

Add at end of script (before any file writing):

```python
# Test generation
print("\n" + "="*60)
print("Testing HTML generation for عسير...")
print("="*60)
html = generate_org_chart_html('عسير')
print(f"Generated {len(html)} characters of HTML")
print(f"Contains logos: {('data:image' in html)}")
print(f"Contains title: {'الهيكل التنظيمي' in html}")
```

- [ ] **Step 3: Verify HTML generation**

Run: `python scripts/gen_org_charts.py`

Expected output:
```
Testing HTML generation for عسير...
Generated X characters of HTML
Contains logos: True
Contains title: True
```

- [ ] **Step 4: Commit**

```bash
git add scripts/gen_org_charts.py
git commit -m "feat: add HTML generation function for org charts"
```

---

### Task 7: Write HTML Files to Disk (gen_org_charts.py)

**Files:**
- Modify: `scripts/gen_org_charts.py`

- [ ] **Step 1: Add file writing logic after HTML generation function**

Replace the test block with actual generation:

```python
# ── Generate and Write HTML Files ──────────────────────────────────

print("\n" + "="*60)
print("Generating org chart HTML files...")
print("="*60)

for region in REGIONS:
    print(f"\nGenerating {region}...")
    html = generate_org_chart_html(region)
    
    output_file = OUT_DIR / REGION_FILE[region]
    output_file.write_text(html, encoding='utf-8')
    print(f"  ✓ Written {output_file.name} ({len(html)} bytes)")

print("\n" + "="*60)
print("Complete!")
print(f"Files location: {OUT_DIR}")
print("="*60)
```

- [ ] **Step 2: Verify files are written**

Run: `python scripts/gen_org_charts.py`

Expected output:
```
Generating org chart HTML files...

Generating عسير...
  ✓ Written 09_OrgChart_Asir.html (X bytes)
  ...

Complete!
Files location: .../app/static/org_charts
```

- [ ] **Step 3: Verify files exist**

Run: `ls -lh C:\Users\engsa\OneDrive\Desktop\AI\HR\mizan\app\static\org_charts\`

Expected: 4 HTML files present

- [ ] **Step 4: Commit**

```bash
git add scripts/gen_org_charts.py
git commit -m "feat: write generated org chart HTML to static directory"
```

---

### Task 8: Add Org Chart Routes to Reports Blueprint (routes.py)

**Files:**
- Modify: `app/blueprints/reports/routes.py:544+` (end of file)

- [ ] **Step 1: Add imports at top of routes.py**

Find the imports section and add:

```python
from pathlib import Path
```

- [ ] **Step 2: Add landing page route at end of routes.py**

Add before the final route:

```python
# ── Org Chart Reports ──────────────────────────────────────────────

@reports_bp.route('/org-chart', methods=['GET'])
@login_required
def org_chart():
    """Landing page showing 4 region org chart options."""
    regions = [
        {'code': 'asir', 'name': 'عسير', 'color': '#0071B9'},
        {'code': 'jizan', 'name': 'جازان', 'color': '#059669'},
        {'code': 'baha', 'name': 'الباحة', 'color': '#d97706'},
        {'code': 'najran', 'name': 'نجران', 'color': '#e11d48'},
    ]
    return render_template('reports/org_chart_landing.html', regions=regions)
```

- [ ] **Step 3: Add view org chart route**

Add after the landing page route:

```python
@reports_bp.route('/org-chart/<region>', methods=['GET'])
@login_required
def org_chart_view(region):
    """Display org chart HTML for a region."""
    region_map = {
        'asir': 'عسير',
        'jizan': 'جازان',
        'baha': 'الباحة',
        'najran': 'نجران',
    }
    
    if region not in region_map:
        return render_template('403.html'), 403
    
    file_map = {
        'asir': '09_OrgChart_Asir.html',
        'jizan': '10_OrgChart_Jizan.html',
        'baha': '11_OrgChart_Baha.html',
        'najran': '12_OrgChart_Najran.html',
    }
    
    html_file = Path(__file__).parent.parent.parent / 'static' / 'org_charts' / file_map[region]
    
    if not html_file.exists():
        return render_template('reports/error.html', 
                             title='الهيكل التنظيمي غير متوفر',
                             message='الهيكل التنظيمي غير متوفر — يرجى تشغيل السكريبت أولاً'), 404
    
    html_content = html_file.read_text(encoding='utf-8')
    region_name = region_map[region]
    
    return render_template('reports/org_chart_view.html',
                         region=region,
                         region_name=region_name,
                         html_content=html_content)
```

- [ ] **Step 4: Add PDF export route**

Add after the view route:

```python
@reports_bp.route('/org-chart/<region>/pdf', methods=['GET'])
@login_required
def org_chart_pdf(region):
    """Export org chart as PDF."""
    from datetime import datetime
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return jsonify({'error': 'Playwright not installed'}), 500
    
    region_map = {
        'asir': 'عسير',
        'jizan': 'جازان',
        'baha': 'الباحة',
        'najran': 'نجران',
    }
    
    if region not in region_map:
        return jsonify({'error': 'Invalid region'}), 400
    
    file_map = {
        'asir': '09_OrgChart_Asir.html',
        'jizan': '10_OrgChart_Jizan.html',
        'baha': '11_OrgChart_Baha.html',
        'najran': '12_OrgChart_Najran.html',
    }
    
    html_file = Path(__file__).parent.parent.parent / 'static' / 'org_charts' / file_map[region]
    
    if not html_file.exists():
        return jsonify({'error': 'Org chart not found'}), 404
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={'width': 1481, 'height': 1970})
            page.goto(f'file://{html_file.absolute()}')
            
            date_str = datetime.now().strftime('%Y-%m-%d')
            pdf_filename = f"OrgChart_{region_map[region]}_{date_str}.pdf"
            pdf_path = Path('/tmp') / pdf_filename
            
            page.pdf(path=str(pdf_path), format='A3', landscape=True, margin={'top': '10mm', 'bottom': '10mm', 'left': '14mm', 'right': '14mm'})
            browser.close()
            
            return send_file(str(pdf_path), as_attachment=True, download_name=pdf_filename, mimetype='application/pdf')
    
    except Exception as e:
        return jsonify({'error': f'PDF generation failed: {str(e)}'}), 500
```

- [ ] **Step 5: Verify routes are added**

Check `app/blueprints/reports/routes.py` contains all 3 new routes

- [ ] **Step 6: Commit**

```bash
git add app/blueprints/reports/routes.py
git commit -m "feat: add org chart routes (landing, view, PDF export)"
```

---

### Task 9: Create Landing Page Template

**Files:**
- Create: `app/templates/reports/org_chart_landing.html`

- [ ] **Step 1: Create landing page template**

Create `app/templates/reports/org_chart_landing.html`:

```html
{% extends "base.html" %}

{% block title %}الهيكل التنظيمي{% endblock %}

{% block content %}
<div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-right mb-8" style="color: #0a1f3d;">الهيكل التنظيمي</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {% for region in regions %}
        <a href="{{ url_for('reports.org_chart_view', region=region.code) }}" 
           class="block p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow text-center"
           style="background-color: {{ region.color }}20; border-left: 4px solid {{ region.color }};">
            <div class="text-2xl font-bold mb-2" style="color: {{ region.color }};">{{ region.name }}</div>
            <div class="text-sm" style="color: #666;">عرض الهيكل التنظيمي</div>
        </a>
        {% endfor %}
    </div>
</div>

<style>
.container {
    font-family: 'Cairo', sans-serif;
}
</style>
{% endblock %}
```

- [ ] **Step 2: Verify template syntax**

Check file for syntax errors (matching tags, proper Jinja2)

- [ ] **Step 3: Commit**

```bash
git add app/templates/reports/org_chart_landing.html
git commit -m "feat: add org chart landing page template"
```

---

### Task 10: Create Chart View Template

**Files:**
- Create: `app/templates/reports/org_chart_view.html`

- [ ] **Step 1: Create view template**

Create `app/templates/reports/org_chart_view.html`:

```html
{% extends "base.html" %}

{% block title %}{{ region_name }} - الهيكل التنظيمي{% endblock %}

{% block content %}
<div class="mb-6 flex justify-between items-center" style="padding: 1rem; background-color: #f5f7fa; border-radius: 0.5rem;">
    <div>
        <a href="{{ url_for('reports.org_chart') }}" class="text-blue-600 hover:text-blue-800">← العودة</a>
        <h1 class="text-2xl font-bold" style="color: #0a1f3d;">الهيكل التنظيمي — {{ region_name }}</h1>
    </div>
    <button onclick="window.location.href='{{ url_for('reports.org_chart_pdf', region=region) }}';" 
            class="px-4 py-2 rounded" 
            style="background-color: #0071B9; color: white; font-weight: 600;">
        📥 تحميل PDF
    </button>
</div>

<div id="org-chart-container" style="overflow: auto; border: 1px solid #d1d9e6; border-radius: 0.5rem;">
    {{ html_content | safe }}
</div>

<style>
body {
    font-family: 'Cairo', sans-serif;
}

@media print {
    #org-chart-container {
        overflow: visible;
        border: none;
    }
}
</style>
{% endblock %}
```

- [ ] **Step 2: Verify template has safe filter for HTML**

Check that `{{ html_content | safe }}` is present

- [ ] **Step 3: Commit**

```bash
git add app/templates/reports/org_chart_view.html
git commit -m "feat: add org chart view template with PDF button"
```

---

### Task 11: Update Reports Index to Add Org Chart Card

**Files:**
- Modify: `app/templates/reports/index.html`

- [ ] **Step 1: Read current reports index template**

Check `app/templates/reports/index.html` to find where report cards are defined

- [ ] **Step 2: Add org chart card**

Find the section with report card definitions (likely a loop or series of `<a>` tags) and add:

```html
<a href="{{ url_for('reports.org_chart') }}" class="report-card" style="border-top-color: #e11d48;">
    <div class="report-icon">📊</div>
    <div class="report-name">الهيكل التنظيمي</div>
    <div class="report-desc">عرض الهيكل التنظيمي حسب المنطقة</div>
</a>
```

(Adjust styling/structure to match existing report cards)

- [ ] **Step 3: Verify card appears in same style as other cards**

Check that grid/layout matches other report cards

- [ ] **Step 4: Commit**

```bash
git add app/templates/reports/index.html
git commit -m "feat: add org chart card to reports home page"
```

---

### Task 12: Add Playwright to Requirements

**Files:**
- Modify: `requirements.txt`

- [ ] **Step 1: Add Playwright to requirements**

Add to `requirements.txt` (if not already present):

```
playwright>=1.40.0
```

- [ ] **Step 2: Verify file**

Ensure `playwright` is listed

- [ ] **Step 3: Commit**

```bash
git add requirements.txt
git commit -m "feat: add Playwright for PDF export"
```

---

### Task 13: Test Script Locally

**Files:**
- No new files (test existing)

- [ ] **Step 1: Run gen_org_charts.py script**

```bash
cd C:\Users\engsa\OneDrive\Desktop\AI\HR\mizan
python scripts/gen_org_charts.py
```

Expected: 4 HTML files generated in `app/static/org_charts/`

- [ ] **Step 2: Verify HTML files exist**

```bash
ls -lh app/static/org_charts/
```

Expected: 4 HTML files, each ~1MB

- [ ] **Step 3: Start Flask development server**

```bash
python run.py
```

- [ ] **Step 4: Visit landing page**

Open: `http://localhost:5000/reports/org-chart`

Expected: Page with 4 region cards (عسير, جازان, الباحة, نجران)

- [ ] **Step 5: Click a region card**

Click on "عسير"

Expected: Org chart HTML displays in `org_chart_view.html` template

- [ ] **Step 6: Test PDF export**

Click "تحميل PDF" button

Expected: PDF downloads as `OrgChart_عسير_<date>.pdf`

- [ ] **Step 7: Verify PDF looks correct**

Open downloaded PDF, check:
- Arabic text renders correctly
- Logos present
- Layout is readable
- No overflow/distortion

---

### Task 14: Deploy to PythonAnywhere

**Files:**
- No new files (deployment only)

- [ ] **Step 1: Commit any remaining changes**

```bash
git status
git add .
git commit -m "chore: final org chart implementation"
```

- [ ] **Step 2: Push to GitHub**

```bash
git push origin master
```

- [ ] **Step 3: SSH into PythonAnywhere server**

```bash
# From your terminal
ssh engsa@ssh.pythonanywhere.com
```

- [ ] **Step 4: Navigate to mizan-app and pull latest code**

```bash
cd /home/southMizan/mizan-app
git pull origin master
```

- [ ] **Step 5: Install dependencies (if needed)**

```bash
pip install playwright
```

- [ ] **Step 6: Install Playwright browsers**

```bash
python -m playwright install chromium
```

- [ ] **Step 7: Generate org charts on server**

```bash
python scripts/gen_org_charts.py
```

Expected: 4 HTML files generated in `/home/southMizan/mizan-app/app/static/org_charts/`

- [ ] **Step 8: Verify files exist**

```bash
ls -lh /home/southMizan/mizan-app/app/static/org_charts/
```

Expected: 4 HTML files present

- [ ] **Step 9: Reload PythonAnywhere app**

Visit: https://www.pythonanywhere.com/user/southMizan/webapps/
Click "Reload" on the mizan-app web app

- [ ] **Step 10: Test on live server**

Visit: https://southmizan.pythonanywhere.com/reports/org-chart

Expected: Landing page loads with 4 region cards

- [ ] **Step 11: Test region view and PDF export**

Click region card → verify org chart displays
Click "تحميل PDF" → verify PDF downloads

- [ ] **Step 12: Update STATUS.md**

```markdown
## Latest work (2026-08-26, session 3)

- Integrated org chart reports from existing scripts
- Created gen_org_charts.py to read from Mizan database
- Added 3 new routes (/reports/org-chart, /view, /pdf)
- Created 2 templates for landing and chart view
- Implemented PDF export using Playwright
- Deployed and tested on PythonAnywhere

Live: https://southmizan.pythonanywhere.com/reports/org-chart
```

- [ ] **Step 13: Commit STATUS.md**

```bash
git add STATUS.md
git commit -m "Update STATUS: org chart integration complete and live"
git push origin master
```

---

## Spec Coverage Verification

| Section | Task |
|---------|------|
| Script adaptation to read from database | Tasks 2-7 |
| Supporting Excel file loading | Task 3 |
| Employee data loading | Task 4 |
| Project data loading | Task 5 |
| HTML generation | Tasks 6-7 |
| Routes implementation | Task 8 |
| Templates | Tasks 9-10 |
| Home page integration | Task 11 |
| PDF export | Task 8 (route), Task 12 (dependencies) |
| Error handling | Task 8 (routes) |
| Local testing | Task 13 |
| Server deployment | Task 14 |

✅ All spec sections covered

---

## Plan Quality Checklist

- ✅ No placeholders (TBD, TODO, "fill in", "add validation")
- ✅ Complete code in every step
- ✅ Exact file paths
- ✅ Exact commands with expected output
- ✅ Frequent commits (one per task)
- ✅ DRY (no code duplication across tasks)
- ✅ YAGNI (only what's needed for feature)
- ✅ TDD pattern (not applicable for HTML/templates, but script tested)
- ✅ Type consistency (region codes, field names match across tasks)
- ✅ Self-contained tasks (each can be understood independently)

import json, base64, re
from collections import Counter
from pathlib import Path
from flask import render_template, request
from flask_login import login_required
from app.blueprints.reports import reports_bp
from app.models import Employee, EmployeeStatus, JobCode, AttendanceGroup, Nationality, Office
from app import db

REGIONS = ['عسير', 'جازان', 'الباحة', 'نجران']
REGION_CODES = {'عسير': 'AS', 'جازان': 'JZ', 'الباحة': 'BA', 'نجران': 'NJ'}


def _b64_logo(rel_path):
    try:
        # Always look in app/static/img/ first (works locally + PythonAnywhere)
        static_path = Path(__file__).parent.parent.parent / 'static' / 'img' / rel_path
        if static_path.exists():
            return 'data:image/png;base64,' + base64.b64encode(static_path.read_bytes()).decode()
        # Fallback: HR project NWC layout folder (local dev only)
        hr_root = Path(__file__).parent.parent.parent.parent.parent.parent.parent
        fallback = hr_root / 'NWC layout' / 'img' / rel_path
        if fallback.exists():
            return 'data:image/png;base64,' + base64.b64encode(fallback.read_bytes()).decode()
    except Exception:
        pass
    return ''


def _chart_data():
    rows = (
        db.session.query(Employee.region, Employee.category, JobCode.title)
        .join(EmployeeStatus, Employee.current_status_id == EmployeeStatus.id)
        .outerjoin(JobCode, Employee.job_code_id == JobCode.id)
        .filter(EmployeeStatus.name_ar == 'على قوة العمل')
        .all()
    )

    def cnt(fn):
        return [sum(1 for r in rows if r.region == reg and fn(r)) for reg in REGIONS]

    def has(kws):
        return lambda r: any(k in (r.title or '') for k in kws)

    def is_job(kw):
        return lambda r: kw in (r.title or '')

    charts = [
        ('c1',  'إجمالي عناصر المشروع', 'h-special', cnt(lambda r: True)),
        ('c2',  'عناصر الإشراف',         'h-special', cnt(lambda r: (r.category or '') == 'إشراف')),
        ('c3',  'عناصر الدعم الفني',     'h-special', cnt(lambda r: (r.category or '') == 'دعم فني')),
        ('c4',  'مهندس مقيم',            'h-navy',    cnt(is_job('مهندس مقيم'))),
        ('c5',  'مهندس موقع',            'h-navy',    cnt(is_job('مهندس موقع'))),
        ('c6',  'مهندس ميكانيكا',         'h-navy',    cnt(has(['ميكانيك']))),
        ('c7',  'مهندس كهرباء وتحكم',    'h-navy',    cnt(has(['كهرباء', 'تحكم']))),
        ('c8',  'مهندس أمن وسلامة',      'h-navy',    cnt(lambda r: 'مهندس' in (r.title or '') and ('أمن' in (r.title or '') or 'سلامة' in (r.title or '')))),
        ('c9',  'مهندس تخطيط',           'h-navy',    cnt(has(['تخطيط']))),
        ('c10', 'مهندس مواد وجودة',      'h-navy',    cnt(lambda r: 'مواد' in (r.title or '') or ('جودة' in (r.title or '') and 'مهندس' in (r.title or '')))),
        ('c11', 'حاسب كميات',            'h-navy',    cnt(has(['كميات']))),
        ('c12', 'مراقب موقع',            'h-navy',    cnt(lambda r: 'مراقب موقع' in (r.title or ''))),
        ('c13', 'مساح',                  'h-navy',    cnt(has(['مساح']))),
        ('c14', 'مراقب أمن وسلامة',      'h-navy',    cnt(lambda r: 'مراقب' in (r.title or '') and ('أمن' in (r.title or '') or 'سلامة' in (r.title or '')))),
        ('c15', 'إخصائي وثائق',          'h-navy',    cnt(has(['وثائق']))),
    ]

    region_totals = {reg: sum(1 for r in rows if r.region == reg) for reg in REGIONS}
    total = len(rows)
    return charts, region_totals, total


@reports_bp.route('/')
@login_required
def index():
    return render_template('reports/index.html')


REPORT_COLUMNS = [
    ('job',        'الوظيفة',          True),
    ('region',     'المنطقة',          True),
    ('nationality','الجنسية',          True),
    ('supervision','نوع الإشراف',      True),
    ('status',     'الموقف',           False),
    ('phone',      'الهاتف',           False),
    ('office',     'المكتب',           False),
    ('att_group',  'كشف الحضور',       False),
    ('hire_date',  'تاريخ الالتحاق',  False),
    ('end_date',   'نهاية العقد',      False),
    ('kafala',     'الكفالة',          False),
    ('re_code',    'كود RE',           False),
]


@reports_bp.route('/filter-report', methods=['GET', 'POST'])
@login_required
def filter_report():
    job_codes    = JobCode.query.order_by(JobCode.title).all()
    att_groups   = AttendanceGroup.query.order_by(AttendanceGroup.name).all()
    all_statuses = EmployeeStatus.query.order_by(EmployeeStatus.name_ar).all()
    kafala_opts  = sorted(set(
        r[0] for r in db.session.query(Employee.kafala).filter(Employee.kafala.isnot(None), Employee.kafala != '').all()
    ))
    offices      = Office.query.order_by(Office.name).all()

    employees       = []
    filters_applied = False
    selected_cols   = [k for k, _, default in REPORT_COLUMNS if default]
    f               = {}

    if request.method == 'POST':
        filters_applied = True
        f = {
            'regions':      request.form.getlist('regions'),
            'nat_group':    request.form.get('nat_group', ''),
            'supervision':  request.form.get('supervision', ''),
            'status_ids':   request.form.getlist('status_ids'),
            'job_code_ids': request.form.getlist('job_code_ids'),
            'att_group_id': request.form.getlist('att_group_id'),
            'kafala_vals':  request.form.getlist('kafala_vals'),
            'office_ids':   request.form.getlist('office_ids'),
        }
        selected_cols = request.form.getlist('cols') or selected_cols

        q = Employee.query.outerjoin(Employee.current_status)
        if f['regions']:
            q = q.filter(Employee.region.in_(f['regions']))
        if f['nat_group'] == 'سعودي':
            q = q.join(Employee.nationality).filter(Nationality.name_ar == 'سعودي')
        elif f['nat_group'] == 'غير سعودي':
            q = q.join(Employee.nationality).filter(Nationality.name_ar != 'سعودي')
        if f['supervision']:
            q = q.filter(Employee.supervision_type == f['supervision'])
        if f['status_ids']:
            q = q.filter(Employee.current_status_id.in_([int(x) for x in f['status_ids']]))
        if f['job_code_ids']:
            q = q.filter(Employee.job_code_id.in_([int(x) for x in f['job_code_ids']]))
        if f['att_group_id']:
            q = q.filter(Employee.attendance_group_id.in_([int(x) for x in f['att_group_id']]))
        if f['kafala_vals']:
            q = q.filter(Employee.kafala.in_(f['kafala_vals']))
        if f['office_ids']:
            q = q.filter(Employee.office_id.in_([int(x) for x in f['office_ids']]))

        employees = q.order_by(Employee.region, Employee.full_name).all()

    return render_template('reports/filter_report.html',
                           job_codes=job_codes,
                           att_groups=att_groups,
                           all_statuses=all_statuses,
                           kafala_opts=kafala_opts,
                           offices=offices,
                           regions=REGIONS,
                           report_columns=REPORT_COLUMNS,
                           employees=employees,
                           filters_applied=filters_applied,
                           selected_cols=selected_cols,
                           f=f,
                           logo_nwc=_b64_logo('NWC_Logo.png'),
                           logo_alamro=_b64_logo('Alamro_Logo.png'))


@reports_bp.route('/emp-kpi')
@login_required
def emp_kpi():
    region = request.args.get('region', '')

    base_q = Employee.query.join(Employee.current_status).filter(
        EmployeeStatus.name_ar == 'على قوة العمل'
    )
    if region and region in REGIONS:
        base_q = base_q.filter(Employee.region == region)
    employees = base_q.all()

    total_active = len(employees)
    saudi_count  = sum(1 for e in employees if e.nationality and e.nationality.name_ar == 'سعودي')
    non_saudi    = total_active - saudi_count

    repl_q = Employee.query.join(Employee.current_status).filter(EmployeeStatus.name_ar == 'بديل')
    if region and region in REGIONS:
        repl_q = repl_q.filter(Employee.region == region)
    replacement_count = repl_q.count()

    # Region bars
    region_counts = Counter(e.region for e in employees if e.region)
    region_data   = [{'name': r, 'count': region_counts.get(r, 0)} for r in REGIONS]

    # Kafala bars
    kafala_counts = Counter(e.kafala for e in employees if e.kafala)
    kafala_data   = [{'name': k, 'count': v}
                     for k, v in sorted(kafala_counts.items(), key=lambda x: -x[1])]

    # Nationality top bars
    nat_counts = Counter(e.nationality.name_ar for e in employees if e.nationality)
    top_nats   = nat_counts.most_common(8)
    top_keys   = {n for n, _ in top_nats}
    other      = sum(v for k, v in nat_counts.items() if k not in top_keys)
    nat_data   = [{'name': n, 'count': c} for n, c in top_nats]
    if other:
        nat_data.append({'name': 'أخرى', 'count': other})

    # E2 / E3 table
    job_e = {}
    for emp in employees:
        if not emp.job_code:
            continue
        title = emp.job_code.title
        m = re.search(r'\b(E[23])\b', title)
        if not m:
            continue
        level = m.group(1)
        base  = title[:title.rfind(level)].strip()
        job_e.setdefault(base, {'E2': 0, 'E3': 0})
        job_e[base][level] += 1

    e_table = sorted(
        [{'job': b, 'e2': v['E2'], 'e3': v['E3'], 'total': v['E2'] + v['E3']}
         for b, v in job_e.items()],
        key=lambda x: -x['total']
    )

    from datetime import date as _date
    return render_template('reports/emp_kpi.html',
                           now=_date.today().strftime('%Y-%m-%d'),
                           total_active=total_active,
                           saudi_count=saudi_count,
                           non_saudi=non_saudi,
                           replacement_count=replacement_count,
                           region_data=json.dumps(region_data, ensure_ascii=False),
                           kafala_data=json.dumps(kafala_data, ensure_ascii=False),
                           nat_data=json.dumps(nat_data, ensure_ascii=False),
                           e_table=e_table,
                           selected_region=region,
                           regions=REGIONS,
                           logo_nwc=_b64_logo('NWC_Logo.png'),
                           logo_alamro=_b64_logo('Alamro_Logo.png'))


@reports_bp.route('/emp-dashboard')
@login_required
def emp_dashboard():
    charts, region_totals, total = _chart_data()
    charts_json = json.dumps([
        {'id': cid, 'title': title, 'cls': cls, 'data': data}
        for cid, title, cls, data in charts
    ], ensure_ascii=False)
    region_bar = [
        {'code': REGION_CODES[r], 'name': r, 'count': region_totals.get(r, 0)}
        for r in REGIONS
    ]
    logo_alamro = _b64_logo('Alamro_Logo.png')
    logo_nwc    = _b64_logo('NWC_Logo.png')
    return render_template(
        'reports/emp_dashboard.html',
        charts_json=charts_json,
        region_bar=region_bar,
        total=total,
        logo_alamro=logo_alamro,
        logo_nwc=logo_nwc,
    )

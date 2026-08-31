from flask import render_template, request, abort, send_file
from flask_login import login_required
from app.blueprints.employees import emp_bp
from app.excel_data import (
    STATUS_ON_STRENGTH, STATUS_REPLACEMENT,
    load_employees, get_employee, employee_statuses,
    SimplePagination, employees_path,
)

REGIONS = ['عسير', 'جازان', 'الباحة', 'نجران']
ACTIVE_STATUSES = {STATUS_ON_STRENGTH, STATUS_REPLACEMENT}
PER_PAGE = 50


def _excel_write_blocked():
    abort(403)


@emp_bp.route('/')
@login_required
def list_employees():
    region = request.args.get('region', '')
    search = request.args.get('q', '').strip()
    status_filter = request.args.get('status', 'active')
    page = request.args.get('page', 1, type=int)

    all_emps = load_employees()
    rows = all_emps

    if status_filter == 'active':
        rows = [e for e in rows if e.current_status and e.current_status.name_ar in ACTIVE_STATUSES]
    elif status_filter != 'all':
        rows = [e for e in rows if e.current_status and e.current_status.name_ar == status_filter]

    if region and region in REGIONS:
        rows = [e for e in rows if e.region == region]
    if search:
        q = search.lower()
        rows = [e for e in rows if q in (e.full_name or '').lower()]

    rows = sorted(rows, key=lambda e: ((e.region or ''), e.full_name or ''))
    total = len(rows)
    page = max(1, page)
    start = (page - 1) * PER_PAGE
    pagination = SimplePagination(rows[start:start + PER_PAGE], page, PER_PAGE, total)

    active_count = sum(1 for e in all_emps if e.current_status and e.current_status.name_ar == STATUS_ON_STRENGTH)
    replacement_count = sum(1 for e in all_emps if e.current_status and e.current_status.name_ar == STATUS_REPLACEMENT)

    return render_template(
        'employees/list.html',
        pagination=pagination,
        regions=REGIONS,
        selected_region=region,
        search=search,
        status_filter=status_filter,
        active_count=active_count,
        replacement_count=replacement_count,
        all_statuses=employee_statuses(all_emps),
    )


@emp_bp.route('/export.xlsx')
@login_required
def export_excel():
    path = employees_path()
    if not path.exists():
        abort(404)
    return send_file(path, as_attachment=True, download_name=path.name)


@emp_bp.route('/<int:emp_id>/panel')
@login_required
def side_panel(emp_id):
    emp = get_employee(emp_id)
    if emp is None:
        abort(404)
    return render_template('employees/_panel.html', emp=emp)


@emp_bp.route('/<int:emp_id>')
@login_required
def profile(emp_id):
    emp = get_employee(emp_id)
    if emp is None:
        abort(404)
    return render_template(
        'employees/profile.html',
        emp=emp,
        statuses=employee_statuses(),
        today='',
    )


@emp_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    _excel_write_blocked()


@emp_bp.route('/<int:emp_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_employee(emp_id):
    _excel_write_blocked()


@emp_bp.route('/<int:emp_id>/status', methods=['POST'])
@login_required
def change_status(emp_id):
    _excel_write_blocked()

from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.blueprints.employees import emp_bp
from app.models import Employee, EmployeeStatus, JobCode, Nationality, Office, AttendanceGroup, EmployeeStatusHistory
from app import db
from datetime import date

REGIONS          = ['عسير', 'جازان', 'الباحة', 'نجران']
STATUS_ON_STRENGTH = 'على قوة العمل'
STATUS_REPLACEMENT = 'بديل'
ACTIVE_STATUSES  = {STATUS_ON_STRENGTH, STATUS_REPLACEMENT}

@emp_bp.route('/')
@login_required
def list_employees():
    region        = request.args.get('region', '')
    search        = request.args.get('q', '').strip()
    status_filter = request.args.get('status', 'active')
    page          = request.args.get('page', 1, type=int)

    q = Employee.query.join(Employee.current_status)

    if status_filter == 'active':
        q = q.filter(EmployeeStatus.name_ar.in_(ACTIVE_STATUSES))
    elif status_filter != 'all':
        q = q.filter(EmployeeStatus.name_ar == status_filter)

    if region and region in REGIONS:
        q = q.filter(Employee.region == region)
    if search:
        q = q.filter(Employee.full_name.contains(search))

    pagination   = q.order_by(Employee.region, Employee.full_name).paginate(page=page, per_page=50)
    active_count = Employee.query.join(Employee.current_status).filter(
        EmployeeStatus.name_ar == STATUS_ON_STRENGTH
    ).count()
    replacement_count = Employee.query.join(Employee.current_status).filter(
        EmployeeStatus.name_ar == STATUS_REPLACEMENT
    ).count()
    all_statuses = EmployeeStatus.query.order_by(EmployeeStatus.name_ar).all()

    return render_template('employees/list.html',
                           pagination=pagination,
                           regions=REGIONS,
                           selected_region=region,
                           search=search,
                           status_filter=status_filter,
                           active_count=active_count,
                           replacement_count=replacement_count,
                           all_statuses=all_statuses)

@emp_bp.route('/<int:emp_id>/panel')
@login_required
def side_panel(emp_id):
    emp = Employee.query.get_or_404(emp_id)
    return render_template('employees/_panel.html', emp=emp)

@emp_bp.route('/<int:emp_id>')
@login_required
def profile(emp_id):
    emp      = Employee.query.get_or_404(emp_id)
    statuses = EmployeeStatus.query.all()
    return render_template('employees/profile.html', emp=emp, statuses=statuses, today=date.today().isoformat())

@emp_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    if current_user.role == 'viewer':
        abort(403)
    statuses      = EmployeeStatus.query.all()
    job_codes     = JobCode.query.order_by(JobCode.title).all()
    nationalities = Nationality.query.order_by(Nationality.name_ar).all()
    offices       = Office.query.order_by(Office.name).all()
    att_groups    = AttendanceGroup.query.order_by(AttendanceGroup.name).all()

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        if not full_name:
            flash('الاسم الكامل مطلوب', 'danger')
            return redirect(url_for('employees.add_employee'))
        emp = Employee(
            full_name           = full_name,
            phone               = request.form.get('phone', '').strip(),
            cbu                 = request.form.get('cbu', '').strip(),
            region              = request.form.get('region', '').strip(),
            job_code_id         = request.form.get('job_code_id') or None,
            unit_price          = request.form.get('unit_price') or None,
            nationality_id      = request.form.get('nationality_id') or None,
            kafala              = request.form.get('kafala', '').strip(),
            office_id           = request.form.get('office_id') or None,
            attendance_group_id = request.form.get('attendance_group_id') or None,
            supervision_type    = request.form.get('supervision_type', '').strip(),
            direct_manager      = request.form.get('direct_manager', '').strip(),
            category            = request.form.get('category', '').strip(),
            hire_date           = _parse_date(request.form.get('hire_date')),
            contract_end_date   = _parse_date(request.form.get('contract_end_date')),
            current_status_id   = request.form.get('current_status_id') or None,
        )
        db.session.add(emp)
        db.session.flush()
        if emp.current_status:
            emp.is_replacement = (emp.current_status.name_ar == STATUS_REPLACEMENT)
            _record_status(emp, None, emp.current_status.name_ar, date.today(), 'إضافة جديدة')
        db.session.commit()
        flash(f'تم إضافة الموظف {emp.full_name}', 'success')
        return redirect(url_for('employees.list_employees'))

    return render_template('employees/add.html',
                           statuses=statuses, job_codes=job_codes,
                           nationalities=nationalities, offices=offices,
                           att_groups=att_groups, regions=REGIONS)

@emp_bp.route('/<int:emp_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_employee(emp_id):
    if current_user.role == 'viewer':
        abort(403)
    emp           = Employee.query.get_or_404(emp_id)
    statuses      = EmployeeStatus.query.all()
    job_codes     = JobCode.query.order_by(JobCode.title).all()
    nationalities = Nationality.query.order_by(Nationality.name_ar).all()
    offices       = Office.query.order_by(Office.name).all()
    att_groups    = AttendanceGroup.query.order_by(AttendanceGroup.name).all()

    # Same-job على قوة العمل employees — for replacement dropdown (بديل only)
    same_job_emps = []
    if emp.is_replacement and emp.job_code_id:
        same_job_emps = (
            Employee.query
            .join(Employee.current_status)
            .filter(
                Employee.job_code_id == emp.job_code_id,
                Employee.id != emp.id,
                EmployeeStatus.name_ar == STATUS_ON_STRENGTH,
            )
            .order_by(Employee.full_name)
            .all()
        )

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        if not full_name:
            flash('الاسم الكامل مطلوب', 'danger')
            return redirect(url_for('employees.edit_employee', emp_id=emp_id))
        emp.full_name             = full_name
        emp.phone                 = request.form.get('phone', '').strip()
        emp.email                 = request.form.get('email', '').strip()
        emp.id_number             = request.form.get('id_number', '').strip()
        emp.cbu                   = request.form.get('cbu', '').strip()
        emp.region                = request.form.get('region', '').strip()
        emp.job_code_id           = request.form.get('job_code_id') or None
        emp.unit_price            = request.form.get('unit_price') or None
        emp.nationality_id        = request.form.get('nationality_id') or None
        emp.kafala                = request.form.get('kafala', '').strip()
        emp.office_id             = request.form.get('office_id') or None
        emp.attendance_group_id   = request.form.get('attendance_group_id') or None
        emp.supervision_type      = request.form.get('supervision_type', '').strip()
        emp.direct_manager        = request.form.get('direct_manager', '').strip()
        emp.category              = request.form.get('category', '').strip()
        emp.hire_date             = _parse_date(request.form.get('hire_date'))
        emp.contract_end_date     = _parse_date(request.form.get('contract_end_date'))
        emp.resignation_date      = _parse_date(request.form.get('resignation_date'))
        emp.profession            = request.form.get('profession', '').strip()
        emp.qualification         = request.form.get('qualification', '').strip()
        emp.grad_year             = request.form.get('grad_year') or None
        emp.experience_years      = request.form.get('experience_years') or None
        emp.serial_no             = request.form.get('serial_no', '').strip()
        emp.re_code               = request.form.get('re_code', '').strip()
        replaced_id               = request.form.get('replaced_employee_id') or None
        emp.replaced_employee_id  = int(replaced_id) if replaced_id else None
        emp.replacement_start_date = _parse_date(request.form.get('replacement_start_date'))
        emp.replacement_end_date   = _parse_date(request.form.get('replacement_end_date'))
        db.session.commit()
        flash(f'تم تحديث بيانات {emp.full_name}', 'success')
        return redirect(url_for('employees.profile', emp_id=emp.id))

    return render_template('employees/edit.html',
                           emp=emp, statuses=statuses, job_codes=job_codes,
                           nationalities=nationalities, offices=offices,
                           att_groups=att_groups, regions=REGIONS,
                           same_job_emps=same_job_emps)

@emp_bp.route('/<int:emp_id>/status', methods=['POST'])
@login_required
def change_status(emp_id):
    if current_user.role == 'viewer':
        abort(403)
    emp           = Employee.query.get_or_404(emp_id)
    new_status_id = request.form.get('new_status_id', type=int)
    reason        = request.form.get('reason', '').strip()
    change_date   = _parse_date(request.form.get('change_date'))
    new_status    = EmployeeStatus.query.get_or_404(new_status_id)
    old_name      = emp.current_status.name_ar if emp.current_status else ''
    emp.current_status_id = new_status_id
    emp.status_reason     = reason
    emp.is_replacement    = (new_status.name_ar == STATUS_REPLACEMENT)
    _record_status(emp, old_name, new_status.name_ar, change_date or date.today(), reason)
    db.session.commit()
    flash(f'تم تغيير حالة {emp.full_name} إلى {new_status.name_ar}', 'success')
    return redirect(url_for('employees.profile', emp_id=emp_id))

# ── helpers ────────────────────────────────────────────────────────────────────

def _parse_date(s):
    try:
        return date.fromisoformat(s) if s else None
    except ValueError:
        return None

def _record_status(emp, old, new, change_date, reason):
    hist = EmployeeStatusHistory(
        employee_id=emp.id,
        old_status=old,
        new_status=new,
        change_date=change_date,
        reason=reason,
        recorded_by=current_user.username if current_user.is_authenticated else 'system',
    )
    db.session.add(hist)

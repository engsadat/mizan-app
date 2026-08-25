from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

# ── Lookup tables ──────────────────────────────────────────────────────────────

class JobCode(db.Model):
    __tablename__ = 'job_codes'
    id             = db.Column(db.Integer, primary_key=True)
    code           = db.Column(db.String(20), unique=True)
    title          = db.Column(db.String(200), nullable=False)
    standard_rate  = db.Column(db.Numeric(10, 2), default=0)
    employees      = db.relationship('Employee', backref='job_code', lazy='dynamic')

class Office(db.Model):
    __tablename__ = 'offices'
    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(200), nullable=False)
    parent_office  = db.Column(db.String(200))
    region         = db.Column(db.String(5))
    attendance_groups = db.relationship('AttendanceGroup', backref='office', lazy='dynamic')

class AttendanceGroup(db.Model):
    __tablename__ = 'attendance_groups'
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(200), nullable=False)
    office_id  = db.Column(db.Integer, db.ForeignKey('offices.id'))

class Nationality(db.Model):
    __tablename__ = 'nationalities'
    id           = db.Column(db.Integer, primary_key=True)
    name_ar      = db.Column(db.String(100), nullable=False)
    country_code = db.Column(db.String(5))
    employees    = db.relationship('Employee', backref='nationality', lazy='dynamic')

class EmployeeStatus(db.Model):
    __tablename__ = 'statuses'
    id      = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(100), nullable=False)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role          = db.Column(db.String(20), default='viewer')
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ── Core tables ────────────────────────────────────────────────────────────────

class Employee(db.Model):
    __tablename__ = 'employees'

    id                   = db.Column(db.Integer, primary_key=True)
    full_name            = db.Column(db.String(400), nullable=False)
    phone                = db.Column(db.String(30))
    email                = db.Column(db.String(200))
    id_number            = db.Column(db.String(50))
    passport             = db.Column(db.String(50))

    nationality_id       = db.Column(db.Integer, db.ForeignKey('nationalities.id'))
    kafala               = db.Column(db.String(200))

    job_code_id          = db.Column(db.Integer, db.ForeignKey('job_codes.id'))
    unit_price           = db.Column(db.Numeric(10, 2))

    cbu                  = db.Column(db.String(5))
    region               = db.Column(db.String(100))
    office_id            = db.Column(db.Integer, db.ForeignKey('offices.id'))
    office               = db.relationship('Office', backref='employees')
    supervision_type     = db.Column(db.String(50))
    attendance_group_id  = db.Column(db.Integer, db.ForeignKey('attendance_groups.id'))
    attendance_group     = db.relationship('AttendanceGroup', backref='employees')

    direct_manager       = db.Column(db.String(200))
    category             = db.Column(db.String(100))
    profession           = db.Column(db.String(200))
    qualification        = db.Column(db.String(200))
    grad_year            = db.Column(db.Integer)
    experience_years     = db.Column(db.Integer)

    hire_date            = db.Column(db.Date)
    contract_end_date    = db.Column(db.Date)
    resignation_date     = db.Column(db.Date)

    current_status_id    = db.Column(db.Integer, db.ForeignKey('statuses.id'))
    current_status       = db.relationship('EmployeeStatus', backref='employees')
    status_reason        = db.Column(db.Text)

    is_replacement         = db.Column(db.Boolean, default=False)
    replaced_employee_id   = db.Column(db.Integer, db.ForeignKey('employees.id'))
    replaced_employee      = db.relationship('Employee', remote_side=[id])
    replacement_start_date = db.Column(db.Date)
    replacement_end_date   = db.Column(db.Date)

    serial_no            = db.Column(db.String(50))
    re_code              = db.Column(db.String(50))

    created_at           = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at           = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    status_history = db.relationship(
        'EmployeeStatusHistory', backref='employee', lazy='dynamic',
        order_by='EmployeeStatusHistory.change_date.desc()'
    )

    def __repr__(self):
        return f'<Employee {self.id} {self.full_name}>'

class EmployeeStatusHistory(db.Model):
    __tablename__ = 'employee_status_history'
    id          = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    old_status  = db.Column(db.String(100))
    new_status  = db.Column(db.String(100), nullable=False)
    change_date = db.Column(db.Date, nullable=False)
    reason      = db.Column(db.Text)
    recorded_by = db.Column(db.String(200))
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)


# ── Finance Data Models (from Excel sources) ──────────────────────────────────

class FinancePO(db.Model):
    """Purchase Order data (PO 1-6)."""
    __tablename__ = 'finance_po'
    id = db.Column(db.Integer, primary_key=True)
    po_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    allocated_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class FinanceInvoice(db.Model):
    """Invoice/Extract data."""
    __tablename__ = 'finance_invoice'
    id = db.Column(db.Integer, primary_key=True)
    invoice_label = db.Column(db.String(50), nullable=False)
    po_number = db.Column(db.Integer, nullable=False, index=True)
    month = db.Column(db.String(50))
    gross_amount = db.Column(db.Float, default=0)
    retention_10 = db.Column(db.Float, default=0)
    vat_amount = db.Column(db.Float, default=0)
    net_amount = db.Column(db.Float, default=0)
    status = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class FinancePO6Job(db.Model):
    """PO 6 job breakdown and variation budget."""
    __tablename__ = 'finance_po6_job'
    id = db.Column(db.Integer, primary_key=True)
    job_no = db.Column(db.Integer, nullable=False, index=True)
    description = db.Column(db.String(500))
    unit_price = db.Column(db.Float, default=0)
    persons = db.Column(db.Float, default=0)
    contract_months = db.Column(db.Float, default=0)
    contract_qty = db.Column(db.Float, default=0)
    contract_total = db.Column(db.Float, default=0)
    cumulative_qty = db.Column(db.Float, default=0)
    cumulative_total = db.Column(db.Float, default=0)
    variation_budget = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

from flask import render_template
from flask_login import login_required
from app.blueprints.main import main_bp
from app.models import Employee, EmployeeStatus
from app import db

@main_bp.route('/')
@login_required
def dashboard():
    active_count = (
        db.session.query(db.func.count(Employee.id))
        .join(EmployeeStatus, Employee.current_status_id == EmployeeStatus.id)
        .filter(EmployeeStatus.name_ar == 'على قوة العمل')
        .scalar() or 0
    )
    monthly_total = (
        db.session.query(db.func.sum(Employee.unit_price))
        .join(EmployeeStatus, Employee.current_status_id == EmployeeStatus.id)
        .filter(EmployeeStatus.name_ar == 'على قوة العمل')
        .scalar() or 0
    )
    monthly_fmt = '{:,.0f}'.format(float(monthly_total))
    return render_template('main/dashboard.html',
                           active_count=active_count,
                           monthly_total=monthly_fmt)


def register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

from flask import render_template
from flask_login import login_required
from app.blueprints.main import main_bp
from app.excel_data import load_employees, STATUS_ON_STRENGTH

@main_bp.route('/')
@login_required
def dashboard():
    emps = [
        e for e in load_employees()
        if e.current_status and e.current_status.name_ar == STATUS_ON_STRENGTH
    ]
    active_count = len(emps)
    monthly_total = sum(e.unit_price or 0 for e in emps)
    monthly_fmt = '{:,.0f}'.format(float(monthly_total))
    return render_template('main/dashboard.html',
                           active_count=active_count,
                           monthly_total=monthly_fmt)


def register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

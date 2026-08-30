from flask import render_template
from flask_login import login_required
from app.blueprints.main import main_bp
from app.excel_data import load_employees, STATUS_ON_STRENGTH


def _home_kpis():
    emps = [
        e for e in load_employees()
        if e.current_status and e.current_status.name_ar == STATUS_ON_STRENGTH
    ]
    monthly_total = sum(e.unit_price or 0 for e in emps)
    return len(emps), '{:,.0f}'.format(float(monthly_total))


@main_bp.route('/')
@login_required
def index():
    active_count, monthly_fmt = _home_kpis()
    return render_template(
        'main/dashboard.html',
        active_count=active_count,
        monthly_total=monthly_fmt,
    )


@main_bp.route('/dashboard')
@login_required
def dashboard():
    return index()


def register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

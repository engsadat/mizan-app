from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from app.blueprints.settings import settings_bp
from app.models import JobCode, User
from app import db


def _admin_only():
    if current_user.role != 'admin':
        abort(403)


@settings_bp.route('/')
@login_required
def index():
    _admin_only()
    return render_template('settings/index.html')

@settings_bp.route('/job-codes')
@login_required
def job_codes():
    _admin_only()
    # Load job codes from Flask config (Excel-backed Phase 1)
    from flask import current_app
    job_codes_dict = current_app.config.get('JOB_CODES', {})

    # Convert dict to list of objects with title, code, and rate attributes
    jcs = [
        type('JobCode', (), {
            'title': title,
            'code': data.get('code', ''),
            'standard_rate': data.get('rate', 0),
            'id': idx
        })()
        for idx, (title, data) in enumerate(sorted(job_codes_dict.items()), 1)
    ]

    return render_template('settings/job_codes.html', job_codes=jcs, edit_jc=None)

@settings_bp.route('/job-codes/add', methods=['POST'])
@login_required
def add_job_code():
    _admin_only()
    title = request.form.get('title', '').strip()
    if not title:
        flash('المسمى الوظيفي مطلوب', 'danger')
        return redirect(url_for('settings.job_codes'))
    jc = JobCode(
        code=request.form.get('code', '').strip() or None,
        title=title,
        standard_rate=request.form.get('standard_rate') or 0,
    )
    db.session.add(jc)
    db.session.commit()
    flash(f'تم إضافة الوظيفة: {jc.title}', 'success')
    return redirect(url_for('settings.job_codes'))

@settings_bp.route('/job-codes/<int:jc_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_job_code(jc_id):
    _admin_only()
    jc = JobCode.query.get_or_404(jc_id)
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if not title:
            flash('المسمى الوظيفي مطلوب', 'danger')
            return redirect(url_for('settings.edit_job_code', jc_id=jc_id))
        jc.code          = request.form.get('code', '').strip() or None
        jc.title         = title
        jc.standard_rate = request.form.get('standard_rate') or 0
        db.session.commit()
        flash(f'تم تحديث الوظيفة: {jc.title}', 'success')
        return redirect(url_for('settings.job_codes'))
    jcs = JobCode.query.order_by(JobCode.title).all()
    return render_template('settings/job_codes.html', job_codes=jcs, edit_jc=jc)

@settings_bp.route('/users')
@login_required
def users():
    _admin_only()
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template('settings/users.html', users=all_users, edit_user=None)

@settings_bp.route('/users/add', methods=['POST'])
@login_required
def add_user():
    _admin_only()
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    role = request.form.get('role', '').strip()

    # Validate
    if not username:
        flash('اسم المستخدم مطلوب', 'danger')
        return redirect(url_for('settings.users'))

    if not password:
        flash('كلمة المرور مطلوبة', 'danger')
        return redirect(url_for('settings.users'))

    if len(password) < 8:
        flash('كلمة المرور يجب أن تكون 8 أحرف على الأقل', 'danger')
        return redirect(url_for('settings.users'))

    if role not in ['admin', 'editor', 'viewer']:
        flash('دور غير صحيح', 'danger')
        return redirect(url_for('settings.users'))

    # Check for duplicate username
    existing = User.query.filter_by(username=username).first()
    if existing:
        flash('اسم المستخدم موجود بالفعل', 'danger')
        return redirect(url_for('settings.users'))

    # Create user
    user = User(
        username=username,
        password_hash=generate_password_hash(password),
        role=role
    )
    db.session.add(user)
    db.session.commit()
    flash(f'تم إضافة المستخدم: {username}', 'success')
    return redirect(url_for('settings.users'))

@settings_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    _admin_only()
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        password = request.form.get('password', '').strip()
        role = request.form.get('role', '').strip()

        # Validate role
        if role not in ['admin', 'editor', 'viewer']:
            flash('دور غير صحيح', 'danger')
            return redirect(url_for('settings.users'))

        # Update password if provided
        if password:
            if len(password) < 8:
                flash('كلمة المرور يجب أن تكون 8 أحرف على الأقل', 'danger')
                return redirect(url_for('settings.users'))
            user.password_hash = generate_password_hash(password)

        # Update role
        user.role = role
        db.session.commit()
        flash(f'تم تحديث المستخدم: {user.username}', 'success')
        return redirect(url_for('settings.users'))

    # GET: show all users with this one highlighted for editing
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template('settings/users.html', users=all_users, edit_user=user)

@settings_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    _admin_only()
    user = User.query.get_or_404(user_id)

    # Prevent self-deletion
    if user.id == current_user.id:
        flash('لا يمكنك حذف حسابك الخاص', 'danger')
        return redirect(url_for('settings.users'))

    # Prevent deleting last admin
    if user.role == 'admin' and User.query.filter_by(role='admin').count() <= 1:
        flash('لا يمكن حذف آخر مسؤول في النظام', 'danger')
        return redirect(url_for('settings.users'))

    username = user.username
    db.session.delete(user)
    db.session.commit()
    flash(f'تم حذف المستخدم: {username}', 'success')
    return redirect(url_for('settings.users'))

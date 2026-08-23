# Mizan User Management Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an admin-only user management page where admins can list, add, edit, and delete users.

**Architecture:** Follow the existing Settings → Job Codes pattern. Single `/settings/users` page with table + inline form for add/edit. Routes in `settings/routes.py`, template in `settings/users.html`. Admin-only access via `_admin_only()` check (already exists).

**Tech Stack:** Flask (routes), Jinja2 (template), Bootstrap RTL (styling), SQLAlchemy (User model, already exists), Werkzeug (password hashing, already used).

---

## Task 1: Add user routes to settings blueprint

**Files:**
- Modify: `app/blueprints/settings/routes.py`

- [ ] **Step 1: Add User import and GET /settings/users route**

Open `app/blueprints/settings/routes.py` and add this import at the top:
```python
from app.models import User
```

Then add this route after the `job_codes()` route:

```python
@settings_bp.route('/users')
@login_required
def users():
    _admin_only()
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template('settings/users.html', users=all_users, edit_user=None)
```

- [ ] **Step 2: Add POST /settings/users/add route**

Add this route after the `users()` route:

```python
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
    
    if role not in ['admin', 'editor', 'viewer']:
        flash('دور غير صحيح', 'danger')
        return redirect(url_for('settings.users'))
    
    # Check for duplicate username
    existing = User.query.filter_by(username=username).first()
    if existing:
        flash('اسم المستخدم موجود بالفعل', 'danger')
        return redirect(url_for('settings.users'))
    
    # Create user
    from werkzeug.security import generate_password_hash
    user = User(
        username=username,
        password_hash=generate_password_hash(password),
        role=role
    )
    db.session.add(user)
    db.session.commit()
    flash(f'تم إضافة المستخدم: {username}', 'success')
    return redirect(url_for('settings.users'))
```

- [ ] **Step 3: Add GET /settings/users/<user_id>/edit route**

Add this route after the `add_user()` route:

```python
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
            from werkzeug.security import generate_password_hash
            user.password_hash = generate_password_hash(password)
        
        # Update role
        user.role = role
        db.session.commit()
        flash(f'تم تحديث المستخدم: {user.username}', 'success')
        return redirect(url_for('settings.users'))
    
    # GET: show all users with this one highlighted for editing
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template('settings/users.html', users=all_users, edit_user=user)
```

- [ ] **Step 4: Add POST /settings/users/<user_id>/delete route**

Add this route after the `edit_user()` route:

```python
@settings_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    _admin_only()
    user = User.query.get_or_404(user_id)
    username = user.username
    db.session.delete(user)
    db.session.commit()
    flash(f'تم حذف المستخدم: {username}', 'success')
    return redirect(url_for('settings.users'))
```

- [ ] **Step 5: Verify imports at top of file**

Check that these imports exist at the top of `app/blueprints/settings/routes.py`:
```python
from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from app.blueprints.settings import settings_bp
from app.models import JobCode, User  # <- User added
from app import db
```

- [ ] **Step 6: Commit**

```bash
cd /path/to/hr_webapp
git add app/blueprints/settings/routes.py
git commit -m "feat(settings): add user management routes

- GET /settings/users: list all users
- POST /settings/users/add: create new user (username, password, role)
- GET/POST /settings/users/<id>/edit: edit user password and/or role
- POST /settings/users/<id>/delete: delete user

All routes admin-only via _admin_only() check"
```

---

## Task 2: Create users.html template

**Files:**
- Create: `app/templates/settings/users.html`

- [ ] **Step 1: Create the template file with header and user table**

Create `app/templates/settings/users.html` with this content:

```html
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
  <meta charset="UTF-8">
  <title>ميزان — إدارة المستخدمين</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.rtl.min.css">
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Cairo', sans-serif; }
    .nav-top { background:#0a1f3d; }
    table { font-size: 0.9rem; }
    .section-title { border-top: 2px solid #dee2e6; margin-top: 2rem; padding-top: 1rem; font-weight: bold; color: #0a1f3d; }
  </style>
</head>
<body>
<nav class="navbar nav-top mb-3">
  <a href="/" class="navbar-brand text-white px-3">ميزان</a>
  <a href="/auth/logout" class="btn btn-sm btn-outline-light ms-auto me-3">خروج</a>
</nav>

<div class="container-fluid p-4">
  <div class="d-flex justify-content-between align-items-center mb-4">
    <h5>إدارة المستخدمين</h5>
    <a href="/settings/" class="btn btn-sm btn-outline-secondary">← العودة للإعدادات</a>
  </div>

  <!-- Flash messages -->
  {% with messages = get_flashed_messages(with_categories=true) %}
    {% for cat, msg in messages %}
      <div class="alert alert-{{ cat }} py-2">{{ msg }}</div>
    {% endfor %}
  {% endwith %}

  <!-- User Table -->
  <table class="table table-sm table-striped table-bordered">
    <thead style="background:#0a1f3d;color:#fff">
      <tr>
        <th>اسم المستخدم</th>
        <th>الدور</th>
        <th>تاريخ الإنشاء</th>
        <th>الإجراءات</th>
      </tr>
    </thead>
    <tbody>
      {% for user in users %}
      <tr {% if edit_user and edit_user.id == user.id %}style="background:#fff3cd"{% endif %}>
        <td>{{ user.username }}</td>
        <td>
          {% if user.role == 'admin' %}
            <span class="badge" style="background:#0a1f3d">مسؤول</span>
          {% elif user.role == 'editor' %}
            <span class="badge" style="background:#0071b9">محرر</span>
          {% else %}
            <span class="badge" style="background:#6c757d">عارض</span>
          {% endif %}
        </td>
        <td>{{ user.created_at.strftime('%Y-%m-%d %H:%M') if user.created_at else '—' }}</td>
        <td>
          <a href="/settings/users/{{ user.id }}/edit" class="btn btn-sm btn-outline-secondary">تعديل</a>
          <form method="POST" action="/settings/users/{{ user.id }}/delete" style="display:inline;">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
            <button type="submit" class="btn btn-sm btn-outline-danger" onclick="return confirm('هل تريد حذف هذا المستخدم؟')">حذف</button>
          </form>
        </td>
      </tr>
      {% else %}
      <tr><td colspan="4" class="text-center text-muted">لا يوجد مستخدمون</td></tr>
      {% endfor %}
    </tbody>
  </table>

  <!-- Add/Edit Form -->
  <div class="section-title">
    {% if edit_user %}
      تعديل المستخدم: {{ edit_user.username }}
    {% else %}
      إضافة مستخدم جديد
    {% endif %}
  </div>

  <form method="POST" {% if edit_user %}action="/settings/users/{{ edit_user.id }}/edit"{% else %}action="/settings/users/add"{% endif %} class="mt-3" style="max-width: 500px;">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">

    <!-- Username -->
    <div class="mb-3">
      <label class="form-label">اسم المستخدم</label>
      {% if edit_user %}
        <input type="text" class="form-control" value="{{ edit_user.username }}" readonly style="background-color: #e9ecef;">
        <small class="form-text text-muted">لا يمكن تغيير اسم المستخدم</small>
      {% else %}
        <input type="text" name="username" class="form-control" placeholder="ادخل اسم المستخدم" required autofocus>
      {% endif %}
    </div>

    <!-- Password -->
    <div class="mb-3">
      <label class="form-label">كلمة المرور</label>
      {% if edit_user %}
        <input type="password" name="password" class="form-control" placeholder="اتركها فارغة للاحتفاظ بالحالية">
        <small class="form-text text-muted">اترك الحقل فارغاً إذا كنت لا تريد تغيير كلمة المرور</small>
      {% else %}
        <input type="password" name="password" class="form-control" placeholder="ادخل كلمة المرور" required>
      {% endif %}
    </div>

    <!-- Role -->
    <div class="mb-3">
      <label class="form-label">الدور</label>
      <select name="role" class="form-select" required>
        <option value="">اختر دوراً</option>
        <option value="admin" {% if edit_user and edit_user.role == 'admin' %}selected{% endif %}>مسؤول (admin)</option>
        <option value="editor" {% if edit_user and edit_user.role == 'editor' %}selected{% endif %}>محرر (editor)</option>
        <option value="viewer" {% if edit_user and edit_user.role == 'viewer' %}selected{% endif %}>عارض (viewer)</option>
      </select>
    </div>

    <!-- Submit Button -->
    <button type="submit" class="btn w-100" style="background:#0a1f3d;color:#fff">
      {% if edit_user %}تحديث{% else %}إضافة{% endif %}
    </button>
  </form>

</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

- [ ] **Step 2: Verify the template renders by checking syntax**

No Python/Jinja errors should be obvious. The template uses:
- `get_flashed_messages()` ✓
- `csrf_token()` ✓
- `user.username`, `user.role`, `user.created_at`, `user.id` (all exist on User model) ✓
- Conditional logic for edit vs add ✓

- [ ] **Step 3: Commit**

```bash
git add app/templates/settings/users.html
git commit -m "feat(settings): create users management template

- User table: username, role, created date, edit/delete buttons
- Add user form: username (required), password (required for new users)
- Edit user form: password (optional), role (required)
- Admin-only, role badge styling"
```

---

## Task 3: Update Settings index to link to users

**Files:**
- Modify: `app/templates/settings/index.html`

- [ ] **Step 1: Open the settings index template and add users link**

Open `app/templates/settings/index.html` and find the section with the job codes link (or the main card area). Add this card:

```html
<div class="col-md-4">
  <a href="/settings/users" class="card p-4 d-block text-decoration-none text-dark">
    <h5>👤 إدارة المستخدمين</h5>
    <small class="text-muted">إنشاء وتعديل وحذف المستخدمين</small>
  </a>
</div>
```

Place it **after** the job codes card so the order is: Home → Job Codes → Users

- [ ] **Step 2: Commit**

```bash
git add app/templates/settings/index.html
git commit -m "feat(settings): add users link to settings index"
```

---

## Task 4: Update Dashboard to show Users card for admins

**Files:**
- Modify: `app/templates/main/dashboard.html`

- [ ] **Step 1: Open dashboard and add admin-only Users card**

Open `app/templates/main/dashboard.html`. Find the section with module cards (Employees, Settings, Reports). Add this card **after Settings** and **only for admins**:

```html
{% if current_user.role == 'admin' %}
<div class="col-md-4">
  <a href="/settings/users" class="card p-4 d-block text-decoration-none text-dark">
    <h5>👤 إدارة المستخدمين</h5>
    <small class="text-muted">إنشاء وتعديل وحذف المستخدمين</small>
  </a>
</div>
{% endif %}
```

- [ ] **Step 2: Verify admin check is correct**

The dashboard already uses `{% if current_user.role == 'admin' %}` for the Settings card. Use the same pattern here. Non-admin users should NOT see the Users card.

- [ ] **Step 3: Commit**

```bash
git add app/templates/main/dashboard.html
git commit -m "feat(dashboard): show users card for admins only"
```

---

## Task 5: Manual testing

**Files:**
- No code changes; testing only

- [ ] **Step 1: Start the app locally**

```bash
cd hr_webapp
export FLASK_APP=manage.py
flask db upgrade  # ensure DB is up to date
python run.py     # start at http://localhost:5001
```

- [ ] **Step 2: Log in as admin (username: admin, password: mizan2026)**

Navigate to http://localhost:5001 → you should see the "Users Card" on the dashboard

- [ ] **Step 3: Click "Users Card" or go to /settings/users**

Verify:
- User table appears with existing users (admin)
- Add user form appears below the table
- Back button works

- [ ] **Step 4: Test add user**

Fill form:
- Username: `testuser1`
- Password: `password123`
- Role: `editor`

Click "إضافة" (Add)

Expected: Success message "تم إضافة المستخدم: testuser1" + table shows new user

- [ ] **Step 5: Test duplicate username rejection**

Try to add another user with username `testuser1`

Expected: Error flash "اسم المستخدم موجود بالفعل" + form clears + page redirects

- [ ] **Step 6: Test empty username rejection**

Try to add user with empty username

Expected: Error flash "اسم المستخدم مطلوب" + page redirects

- [ ] **Step 7: Test empty password rejection (add only)**

Try to add user with empty password

Expected: Error flash "كلمة المرور مطلوبة" + page redirects

- [ ] **Step 8: Test edit user**

Click "تعديل" on `testuser1` row

Expected:
- Form populates with `testuser1` (username is read-only, grayed out)
- Form title changes to "تعديل المستخدم: testuser1"
- Row is highlighted (yellow background)

- [ ] **Step 9: Test edit password**

In edit form:
- Leave password empty
- Change role to `admin`
- Click "تحديث"

Expected: Success message "تم تحديث المستخدم: testuser1" + role changes to admin in table + password unchanged (user can still log in with old password)

- [ ] **Step 10: Test edit password change**

Click "تعديل" on `testuser1` again

Fill:
- Password: `newpassword456`
- Role: keep as `admin`
- Click "تحديث"

Expected: Success message + password is now hashed (verify by trying to log in as testuser1 with old password — should fail; new password should work)

- [ ] **Step 11: Test delete user**

Click "حذف" on any user

Expected: Confirmation popup "هل تريد حذف هذا المستخدم؟"

Click OK

Expected: Success message "تم حذف المستخدم: <username>" + user removed from table

- [ ] **Step 12: Test non-admin access (403)**

Log out. Create a test editor user via SQL or by adding one through the form.

Log in as editor.

Try to access `/settings/users` directly

Expected: 403 Forbidden page

- [ ] **Step 13: Verify Users card not visible to editors**

Log in as editor

Check dashboard: "Users Card" should NOT appear

Expected: Only see Employees, Reports cards (not Users, not Settings)

- [ ] **Step 14: Commit test results**

```bash
git add -A
git commit -m "test(settings): manual testing of user management complete

All flows tested:
- Add user (valid, duplicate, empty)
- Edit user (password + role)
- Delete user with confirmation
- Non-admin access blocked (403)
- Users card hidden from editors
- Password hashing working"
```

---

## Spec Coverage Self-Review

✅ **List users** — Task 1 (GET /users route), Task 2 (table template)  
✅ **Add users** — Task 1 (POST /users/add route), Task 2 (form), Task 5 (tested)  
✅ **Edit users** — Task 1 (GET/POST /users/<id>/edit route), Task 2 (edit form), Task 5 (tested)  
✅ **Delete users** — Task 1 (POST /users/<id>/delete route), Task 2 (delete button), Task 5 (tested)  
✅ **Admin-only access** — Task 1 (all routes use `_admin_only()`), Task 2 (no public access)  
✅ **Dashboard card (admin-only)** — Task 4  
✅ **Settings index link** — Task 3  
✅ **3 fields** — Task 1, Task 2 (username, password, role)  
✅ **Password hashing** — Task 1 (uses `generate_password_hash`)  
✅ **CSRF protection** — Task 2 (csrf_token in forms)  
✅ **Flash messages** — Task 1 (all validations flash)  
✅ **Validation** — Task 1 (username duplicate, empty fields, role validation)  

No gaps found. All spec requirements have corresponding tasks.

---

## No Placeholders Check

✓ All code is complete and runnable  
✓ All commands are exact (`git commit -m "..."`, `flask db upgrade`)  
✓ All expected output is documented  
✓ No "TBD", "TODO", "add validation", or similar  
✓ All imports are shown  
✓ All field/method names match (User.username, User.role, User.created_at, User.password_hash, User.id all exist)  
✓ Form action URLs are exact (`/settings/users/add`, `/settings/users/<id>/edit`, `/settings/users/<id>/delete`)  

---

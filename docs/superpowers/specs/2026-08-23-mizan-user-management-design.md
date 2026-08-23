# Mizan User Management — Design Spec

**Date:** 2026-08-23  
**Scope:** Admin-only user CRUD interface for Mizan  
**Status:** Design approved, ready for implementation

---

## Overview

Add a user management page to Mizan's Settings section. Admins will be able to:
- List all users
- Add new users (username, password, role)
- Edit users (change password and/or role)
- Delete users with confirmation

The feature follows the existing **Settings → Job Codes** pattern: single page with a table and inline add/edit form.

---

## User Roles & Access Control

| Role | Permissions |
|---|---|
| **Admin** | Manage users + settings. Can see Users card on dashboard. |
| **Editor** | Manage employees only. No access to user management. |
| **Viewer** | Read-only. No access to user management. |

Implementation: `@login_required` + `_admin_only()` check (already exists in settings routes).

---

## Data Model

**User Table (existing `users` table)**
```
id              INTEGER PRIMARY KEY
username        VARCHAR(80) UNIQUE NOT NULL
password_hash   VARCHAR(256)
role            VARCHAR(20) DEFAULT 'viewer' (admin|editor|viewer)
created_at      DATETIME DEFAULT now()
```

**Fields to display:** username, role, created_at (formatted as YYYY-MM-DD HH:MM)

---

## Routes

### `/settings/users` (GET)
**Purpose:** Display user list + add/edit form  
**Access:** Admin only  
**Response:** Render `settings/users.html` with:
- `users` — all User records, ordered by created_at DESC
- `edit_user` — None (or User object if editing)

### `/settings/users/add` (POST)
**Purpose:** Create new user  
**Access:** Admin only  
**Form fields:**
- `username` (string, required, unique) → validate, flash error if duplicate
- `password` (string, required, min 4 chars) → hash with `generate_password_hash()`
- `role` (string, required, one of: admin|editor|viewer) → validate dropdown

**Response:** Redirect to `/settings/users` with success flash  
**Error handling:**
- Empty username → flash "اسم المستخدم مطلوب" + redirect
- Duplicate username → flash "اسم المستخدم موجود بالفعل" + redirect
- Empty password → flash "كلمة المرور مطلوبة" + redirect
- Invalid role → flash "دور غير صحيح" + redirect

### `/settings/users/<user_id>/edit` (GET or POST)
**Purpose:** Display edit form OR update user  
**Access:** Admin only  
**GET response:** Render `settings/users.html` with `edit_user=<User>`  
**POST behavior:**
- `username` is read-only (display only, not in form input)
- `password` (optional if editing) → if provided, hash and update; if empty, keep existing
- `role` (required) → update if changed

**Response:** Redirect to `/settings/users` with success flash  
**Special case:** If admin is trying to edit themselves and changes their own role, still allow it (no self-lock protection).

### `/settings/users/<user_id>/delete` (POST)
**Purpose:** Delete a user with confirmation  
**Access:** Admin only  
**Implementation:** Include delete button in table with inline `onclick="return confirm('...')"` JavaScript confirmation  
**Response:** Redirect to `/settings/users` with success flash  
**Edge case:** Deleting self is allowed (admin can lock themselves out; recovery requires DB access).

---

## Template: `app/templates/settings/users.html`

### Layout
```
Header: الموظفون والأدوار (Users & Roles)

[User Table]
username | role | created_at | [Edit] [Delete]
----------+------+------------+---------
admin    | admin| 2026-08-15 | [Edit] [Delete]
...

[Form: Add/Edit User]
IF edit_user is None:
  Heading: إضافة موظف جديد (Add User)
ELSE:
  Heading: تعديل الموظف: {edit_user.username}

Fields:
- اسم المستخدم (Username)
  IF editing: readonly (display only, no input)
  IF adding: text input, required
  
- كلمة المرور (Password)
  IF adding: text input, required, type=password
  IF editing: text input, optional, type=password, placeholder="اتركها فارغة للاحتفاظ بالحالية"
  
- الدور (Role)
  dropdown, required
  Options: admin | editor | viewer
  Selected = current role

- [Button: حفظ (Save)] 
  OR [Button: إضافة (Add)]
```

### Styling
- Use Bootstrap RTL (already included)
- Match existing settings pages (job_codes.html)
- Table: table-striped, small
- Buttons: btn-outline-secondary for Edit, btn-outline-danger for Delete
- Form section: border-top, margin-top: 2rem

---

## Dashboard Integration

**File:** `app/templates/main/dashboard.html`

Add Users card visible **only to admins:**
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

---

## Settings Index Link

**File:** `app/templates/settings/index.html`

Add link or card:
```html
<a href="/settings/users" class="card p-4 d-block text-decoration-none text-dark">
  <h5>👤 إدارة المستخدمين</h5>
  <small class="text-muted">إنشاء وتعديل وحذف المستخدمين</small>
</a>
```

---

## Flash Messages

| Action | Message |
|---|---|
| User added | `تم إضافة المستخدم: {username}` (success) |
| User edited | `تم تحديث المستخدم: {username}` (success) |
| User deleted | `تم حذف المستخدم: {username}` (success) |
| Duplicate username | `اسم المستخدم موجود بالفعل` (danger) |
| Empty username | `اسم المستخدم مطلوب` (danger) |
| Empty password (add) | `كلمة المرور مطلوبة` (danger) |
| Invalid role | `دور غير صحيح` (danger) |

---

## Testing Checklist

- [ ] Admin can view user list
- [ ] Admin can add user (valid data)
- [ ] Add user rejects duplicate username
- [ ] Add user rejects empty username/password
- [ ] Admin can edit user (change role)
- [ ] Admin can edit user (change password)
- [ ] Admin can edit user (keep password empty = no change)
- [ ] Edit form shows username as read-only
- [ ] Admin can delete user with confirmation
- [ ] Users card appears on admin dashboard
- [ ] Users card does NOT appear on editor/viewer dashboard
- [ ] Non-admin cannot access `/settings/users` (403)

---

## Implementation Order

1. Add routes (`/users`, `/users/add`, `/users/<id>/edit`, `/users/<id>/delete`) to `settings/routes.py`
2. Create `users.html` template
3. Update dashboard to show Users card for admins
4. Update settings index page
5. Test all flows

---

## Known Constraints

- **No email field:** Just username + password + role
- **Password recovery:** If admin forgets, admin with DB access must manually reset
- **No rate limiting on password attempts:** Assume internal/trusted users
- **No audit log:** Who created/edited users is not tracked (can be added later)
- **Edit form on same page:** Not separate routes (matches job codes pattern)

---

## Future Enhancements (Out of Scope)

- Email-based password reset
- Password strength meter
- Last login tracking
- Audit log of user changes
- Bulk user import

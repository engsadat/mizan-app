from app.models import User
from app import db


def _login(client, app, username, role, password='pw'):
    with app.app_context():
        if User.query.filter_by(username=username).first() is None:
            u = User(username=username, role=role)
            u.set_password(password)
            db.session.add(u)
            db.session.commit()
    client.post('/auth/login', data={'username': username, 'password': password})


def test_admin_home_has_three_doors_not_users_card(app, client):
    _login(client, app, 'admin', 'admin')
    body = client.get('/').data.decode('utf-8')
    assert 'الموظفون' in body
    assert 'التقارير' in body
    assert 'الإعدادات' in body
    assert '/settings/users' not in body
    assert body.count('href="/employees/"') >= 1
    assert body.count('href="/reports/"') >= 1
    assert body.count('href="/settings/"') >= 1


def test_viewer_home_hides_settings(app, client):
    _login(client, app, 'view1', 'viewer')
    body = client.get('/').data.decode('utf-8')
    assert 'الموظفون' in body
    assert 'التقارير' in body
    assert 'href="/settings/"' not in body

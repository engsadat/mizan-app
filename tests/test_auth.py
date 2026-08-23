from app.models import User
from app import db

def test_app_creates(app):
    assert app is not None

def _make_user(app, username='admin', password='secret'):
    with app.app_context():
        u = User(username=username)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()

def test_login_page_loads(client):
    r = client.get('/auth/login')
    assert r.status_code == 200
    assert 'تسجيل الدخول' in r.data.decode('utf-8')

def test_login_success(app, client):
    _make_user(app)
    r = client.post('/auth/login', data={'username': 'admin', 'password': 'secret'}, follow_redirects=True)
    assert r.status_code == 200
    assert 'لوحة التحكم' in r.data.decode('utf-8')

def test_login_wrong_password(app, client):
    _make_user(app)
    r = client.post('/auth/login', data={'username': 'admin', 'password': 'wrong'}, follow_redirects=True)
    assert 'بيانات خاطئة' in r.data.decode('utf-8')

def test_logout_redirects(app, client):
    _make_user(app)
    client.post('/auth/login', data={'username': 'admin', 'password': 'secret'})
    r = client.get('/auth/logout', follow_redirects=True)
    assert 'تسجيل الدخول' in r.data.decode('utf-8')

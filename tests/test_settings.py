from app.models import User, JobCode
from app import db

def _login(client, app):
    with app.app_context():
        u = User(username='admin', role='admin')
        u.set_password('pw')
        db.session.add(u)
        db.session.commit()
    client.post('/auth/login', data={'username': 'admin', 'password': 'pw'})

def test_settings_index_loads(app, client):
    _login(client, app)
    r = client.get('/settings/')
    assert r.status_code == 200
    assert 'الإعدادات' in r.data.decode('utf-8')

def test_add_job_code(app, client):
    _login(client, app)
    r = client.post('/settings/job-codes/add', data={
        'code': 'JOB099',
        'title': 'مراقب أمن وسلامة',
        'standard_rate': '250',
    }, follow_redirects=True)
    assert r.status_code == 200
    with app.app_context():
        jc = JobCode.query.filter_by(code='JOB099').first()
        assert jc is not None
        assert jc.title == 'مراقب أمن وسلامة'

def test_job_codes_list_shows_entry(app, client):
    _login(client, app)
    with app.app_context():
        db.session.add(JobCode(code='J001', title='مهندس مقيم', standard_rate=300))
        db.session.commit()
    r = client.get('/settings/job-codes')
    assert 'مهندس مقيم' in r.data.decode('utf-8')

from tests.test_dashboard_cards import _login


def test_reports_index(app, client):
    _login(client, app, 'ed1', 'editor')
    r = client.get('/reports/')
    body = r.data.decode('utf-8')
    assert r.status_code == 200
    assert 'لوحة إحصاءات' in body
    assert 'قابل للطباعة' in body
    assert '/reports/emp-dashboard' in body
    assert '/reports/filter-report' in body

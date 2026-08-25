from tests.test_dashboard_cards import _login


def test_viewer_settings_403(app, client):
    _login(client, app, 'view2', 'viewer')
    assert client.get('/settings/').status_code == 403
    assert client.get('/settings/users').status_code == 403
    assert client.get('/settings/job-codes').status_code == 403


def test_settings_hub_two_links_only(app, client):
    _login(client, app, 'admin2', 'admin')
    body = client.get('/settings/').data.decode('utf-8')
    assert '/settings/job-codes' in body
    assert '/settings/users' in body
    assert '/settings/offices' not in body
    assert 'data_maintenance' not in body

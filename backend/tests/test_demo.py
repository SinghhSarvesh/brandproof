import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import app as a
import seed


@pytest.fixture
def demo(monkeypatch):
    engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    factory = sessionmaker(engine, expire_on_commit=False)
    for module in (a, seed):
        monkeypatch.setattr(module, 'engine', engine)
        monkeypatch.setattr(module, 'SessionLocal', factory)
    monkeypatch.setenv('DEMO_PASSWORD', 'synthetic-test-password')
    monkeypatch.delenv('DEMO_QUICK_FILL', raising=False)
    with TestClient(a.app) as client:
        yield client, factory


def test_demo_opt_in_and_all_roles(demo, monkeypatch):
    client, _ = demo
    seed.seed()
    assert client.get('/api/demo-accounts').json() == {'accounts': []}
    monkeypatch.setenv('DEMO_QUICK_FILL', 'true')
    response = client.get('/api/demo-accounts')
    assert response.headers['cache-control'] == 'no-store'
    accounts = response.json()['accounts']
    assert [x['role'] for x in accounts] == ['manager', 'creator', 'reviewer']
    for account in accounts:
        result = client.post('/api/login', json=account)
        assert result.status_code == 200
        assert result.json()['role'] == account['role']


def test_password_sync_is_opt_in_and_preserves_other_users(demo, monkeypatch):
    client, factory = demo
    seed.seed()
    with factory() as session:
        session.add(a.User(email='private@example.test', org='private', role='manager', password=a.password_hash('private-test-password')))
        session.commit()
    monkeypatch.setenv('DEMO_PASSWORD', 'replacement-test-password')
    seed.seed()
    monkeypatch.setenv('DEMO_QUICK_FILL', 'true')
    assert client.get('/api/demo-accounts').json() == {'accounts': []}
    seed.seed()
    assert len(client.get('/api/demo-accounts').json()['accounts']) == 3
    assert client.post('/api/login', json={'email': 'private@example.test', 'password': 'private-test-password'}).status_code == 200
    with factory() as session:
        user = session.scalar(select(a.User).where(a.User.email == 'manager@brandproof.demo'))
        user.org = 'private'
        session.commit()
    assert len(client.get('/api/demo-accounts').json()['accounts']) == 2
    with pytest.raises(SystemExit, match='identity mismatch'):
        seed.seed()

"""Real PostgreSQL integration races; never simulate PostgreSQL locks with SQLite."""
import os
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
import pytest
from test_workflow import ctx, source, draft, review, request, approve
from test_round3 import correction

pytestmark = pytest.mark.skipif(not os.getenv('TEST_DATABASE_URL'), reason='Requires isolated PostgreSQL test database')


def race(*actions):
    gate = Barrier(len(actions))
    def execute(fn):
        gate.wait(timeout=10)
        return fn()
    with ThreadPoolExecutor(max_workers=len(actions)) as pool:
        return list(pool.map(execute, actions))


def test_parallel_corrections_only_one_wins(ctx):
    c, h = ctx
    source(c, h)
    sub, _ = draft(c, h, 'Enjoy 20 hours of battery life.')
    body = correction(c, h, sub, review(c, h, sub).json())
    def apply(): return c.post('/api/corrections/apply', json=body, headers=h['creator'])
    assert sorted(r.status_code for r in race(apply, apply)) == [200, 409]


def test_parallel_reviewer_decisions_only_one_wins(ctx):
    c, h = ctx
    source(c, h)
    sub, _ = draft(c, h)
    review(c, h, sub); request(c, h, sub)
    assert sorted(r.status_code for r in race(lambda: approve(c, h, sub), lambda: approve(c, h, sub))) == [200, 409]


def test_revision_races_approval_no_stale_approval(ctx):
    c, h = ctx
    source(c, h)
    sub, b = draft(c, h)
    review(c, h, sub); request(c, h, sub)
    def edit(): return c.post(f"/api/submissions/{sub['id']}/revisions", json={**b, 'text': 'Changed draft', 'expected_revision_id': sub['latest_revision']}, headers=h['creator'])
    results = race(edit, lambda: approve(c, h, sub))
    assert results[0].status_code == 200
    assert results[1].status_code in (200, 409)
    final = c.get(f"/api/submissions/{sub['id']}", headers=h['reviewer']).json()
    assert final['status'] == 'draft'
    assert all(x['revision_id'] != final['latest_revision'] for x in final['approvals'])


def test_source_races_approval_requires_revalidation(ctx):
    c, h = ctx
    src = source(c, h)
    sub, _ = draft(c, h)
    review(c, h, sub); request(c, h, sub)
    results = race(lambda: source(c, h, text='Up to 10 hours of battery life.', supersedes=src['id']), lambda: approve(c, h, sub))
    assert results[1].status_code in (200, 409)
    final = c.get(f"/api/submissions/{sub['id']}", headers=h['reviewer']).json()
    assert final['status'] == 'revalidation_required'

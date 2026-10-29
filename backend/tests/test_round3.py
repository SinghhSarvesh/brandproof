from datetime import date, timedelta
from test_workflow import ctx, source, draft, review, request, approve
import app as a


def correction(c, h, sub, run):
    f = run['findings'][0]
    text = c.get(f"/api/submissions/{sub['id']}", headers=h['creator']).json()['revisions'][0]['text']
    return dict(review_id=run['id'], revision_id=sub['latest_revision'], index=0,
                start=text.index(f['quote']), replacement=f['suggestion'], reason='Verified intent')


def test_exact_correction_new_revision_stale_and_permission(ctx):
    c, h = ctx
    source(c, h)
    sub, _ = draft(c, h, 'Enjoy 20 hours of battery life. Keep the launch message.')
    body = correction(c, h, sub, review(c, h, sub).json())
    preview = c.post('/api/corrections/preview', json=body, headers=h['creator'])
    assert preview.status_code == 200, preview.text
    assert preview.json()['after'] == 'Enjoy up to 12 hours of battery life. Keep the launch message.'
    assert c.post('/api/corrections/apply', json=body, headers=h['reviewer']).status_code == 403
    assert c.post('/api/corrections/apply', json=body, headers=h['other']).status_code == 404
    saved = c.post('/api/corrections/apply', json=body, headers=h['creator'])
    assert saved.status_code == 200
    assert saved.json()['id'] != sub['latest_revision']
    assert c.post('/api/corrections/apply', json=body, headers=h['creator']).status_code == 409
    assert request(c, h, sub).status_code == 409


def test_correction_numbers_qualifiers_and_offsets(ctx):
    c, h = ctx
    source(c, h)
    sub, _ = draft(c, h, 'Enjoy 20 hours of battery life.')
    body = correction(c, h, sub, review(c, h, sub).json())
    for replacement in ['up to 99 hours', '12 hours']:
        assert c.post('/api/corrections/preview', json={**body, 'replacement': replacement}, headers=h['creator']).status_code == 422
    assert c.post('/api/corrections/apply', json={**body, 'start': 0}, headers=h['creator']).status_code == 409


def test_select_second_occurrence(ctx):
    c, h = ctx
    source(c, h, kind='term', title='Name', text='Use Northstar One.', match='NS1', replacement='Northstar One')
    sub, _ = draft(c, h, 'NS1 launches today. Discover NS1.')
    body = correction(c, h, sub, review(c, h, sub).json())
    body['start'] = 'NS1 launches today. Discover NS1.'.rindex('NS1')
    preview = c.post('/api/corrections/preview', json=body, headers=h['creator'])
    assert preview.json()['after'] == 'NS1 launches today. Discover Northstar One.'
    assert c.post('/api/corrections/preview', json={**body, 'replacement': 'OtherPhone'}, headers=h['creator']).status_code == 422


def test_unrelated_source_keeps_approval_related_invalidates_once(ctx):
    c, h = ctx
    src = source(c, h)
    sub, _ = draft(c, h)
    review(c, h, sub); request(c, h, sub)
    assert approve(c, h, sub).status_code == 200
    source(c, h, title='Warranty', text='Warranty lasts 2 years.', match='warranty')
    assert c.get('/api/submissions', headers=h['creator']).json()[0]['status'] == 'approved'
    source(c, h, text='Up to 10 hours of battery life.', supersedes=src['id'])
    assert c.get('/api/submissions', headers=h['creator']).json()[0]['status'] == 'revalidation_required'
    for _ in range(2):
        notes = c.get('/api/notifications', headers=h['reviewer']).json()
        assert len(notes) == 1
    assert c.get('/api/notifications', headers=h['other']).json() == []
    assert c.post(f"/api/notifications/{notes[0]['id']}/read", json={}, headers=h['reviewer']).status_code == 200
    assert c.get('/api/notifications', headers=h['reviewer']).json()[0]['read']
    evidence = c.get(f"/api/submissions/{sub['id']}/evidence", headers=h['reviewer']).json()
    assert evidence['approvals'][0]['source_dependencies'][0]['id'] == src['id']


def test_expiry(ctx, monkeypatch):
    c, h = ctx
    today = date.today()
    source(c, h, valid_until=today.isoformat())
    sub, _ = draft(c, h)
    review(c, h, sub); request(c, h, sub); approve(c, h, sub)
    class Tomorrow(date):
        @classmethod
        def today(cls): return today + timedelta(days=1)
    monkeypatch.setattr(a, 'date', Tomorrow)
    assert c.get('/api/submissions', headers=h['reviewer']).json()[0]['status'] == 'revalidation_required'


def test_conflicts_block_approval_and_visible_ranking(ctx):
    c, h = ctx
    source(c, h)
    source(c, h, text='Up to 18 hours of battery life.')
    sub, _ = draft(c, h)
    run = review(c, h, sub).json()
    assert run['status'] == 'incomplete'
    assert len(run['conflicts']) == 1
    assert run['retrieval'][0]['reason'] == 'structured match'
    assert request(c, h, sub).status_code == 409


def test_edit_optimistic_concurrency(ctx):
    c, h = ctx
    sub, b = draft(c, h)
    body = {**b, 'expected_revision_id': sub['latest_revision'], 'text': 'First editor'}
    assert c.post(f"/api/submissions/{sub['id']}/revisions", json=body, headers=h['creator']).status_code == 200
    assert c.post(f"/api/submissions/{sub['id']}/revisions", json={**body, 'text': 'Second editor'}, headers=h['creator']).status_code == 409


def test_existing_qualifier_not_duplicated(ctx):
    c,h = ctx
    source(c,h)
    sub,_ = draft(c,h,'Enjoy up to 20 hours of battery life.')
    body = correction(c,h,sub,review(c,h,sub).json())
    result = c.post('/api/corrections/apply',json=body,headers=h['creator'])
    assert result.status_code == 200, result.text
    assert result.json()['text'] == 'Enjoy up to 12 hours of battery life.'

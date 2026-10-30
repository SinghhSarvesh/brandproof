import json
import pytest
import app

SOURCE = dict(id=7, kind='term', title='Naming', text='Use Cedar Two as the product name.',
              match='C2', replacement='Cedar Two', version=1)
REV = dict(text='Meet C2 today.', purpose='Announce Cedar Two', audience='Buyers')

def payload(**kw):
    return json.dumps({'findings': [dict(category='messaging',quote='C2',source_id=7,
        evidence=SOURCE['text'],explanation='Use the approved name.',suggestion='Cedar Two',
        severity='medium',**kw)]})

def test_naming_has_one_category_and_duplicate_overlap_is_coalesced():
    found=app.validate_semantic(payload(),REV,[SOURCE])
    assert found[0]['category']=='terminology'
    other={**found[0],'quote':'Meet C2 today.'}
    assert len(app.deduplicate(found+[other]))==1
    distinct={**found[0],'source_id':8}
    assert len(app.deduplicate(found+[distinct]))==2

def test_exact_evidence_remains_strict():
    for change in ({'evidence':'Invented rule'},{'quote':'Cedar Two'},{'source_id':99}):
        body=json.loads(payload());body['findings'][0].update(change)
        with pytest.raises(ValueError):app.validate_semantic(json.dumps(body),REV,[SOURCE])

def fake_provider(monkeypatch,outputs):
    calls=[]
    class Response:
        def raise_for_status(self):pass
        def json(self):return {'choices':[{'message':{'content':outputs[len(calls)-1]}}]}
    class Client:
        def __init__(self,**kw):pass
        def __enter__(self):return self
        def __exit__(self,*args):pass
        def post(self,*args,**kw):calls.append(kw);return Response()
    monkeypatch.setattr(app.httpx,'Client',Client)
    monkeypatch.setenv('AI_API_KEY','test');monkeypatch.setenv('AI_MODEL','test')
    return calls

def test_one_invalid_response_can_be_repaired_without_dropping_real_issue(monkeypatch):
    calls=fake_provider(monkeypatch,['not JSON',payload()])
    result=app.semantic(REV,[SOURCE])
    assert len(calls)==2
    assert result[0]['category']=='terminology'

def test_two_invalid_responses_fail_closed(monkeypatch):
    calls=fake_provider(monkeypatch,['not JSON','not JSON'])
    with pytest.raises(ValueError):app.semantic(REV,[SOURCE])
    assert len(calls)==2

def test_clean_review_is_not_retried(monkeypatch):
    calls=fake_provider(monkeypatch,['{"findings":[]}'])
    assert app.semantic(REV,[SOURCE])==[]
    assert len(calls)==1

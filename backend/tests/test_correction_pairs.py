import json
from pathlib import Path
import pytest
from test_workflow import ctx, source, draft, review
from test_round3 import correction

PAIRS = json.loads((Path(__file__).resolve().parents[2] / 'evaluation/corrections.json').read_text())['cases']


@pytest.mark.parametrize('pair', PAIRS, ids=lambda x:x['id'])
def test_correction_pair(ctx, pair):
    c,h = ctx
    if pair['kind'] == 'term':
        source(c,h,kind='term',text='Use Northstar One.',match='NS1',replacement='Northstar One')
    elif pair['kind'] == 'claim':
        source(c,h,kind='claim',text='No unsupported rankings.',match='No. 1',replacement='')
    else:
        source(c,h)
    sub,_ = draft(c,h,pair['before'])
    body = correction(c,h,sub,review(c,h,sub).json())
    body['replacement'] = pair['replacement']
    response = c.post('/api/corrections/apply',json=body,headers=h['creator'])
    assert response.status_code == pair['status'], response.text
    if pair['after'] is not None:
        assert response.json()['text'] == pair['after']

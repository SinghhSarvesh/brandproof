"""Evaluate the deployed synthetic demo without exposing credentials or provider keys.
Creates labelled synthetic submissions; does not alter sources or approve content.
"""
import argparse, json, time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
import httpx

ROOT=Path(__file__).resolve().parents[1]

def run(base,output):
    fixture=json.loads((ROOT/'evaluation/submissions.json').read_text())
    result={'started_at':datetime.now(timezone.utc).isoformat(),'url':base,
            'unit':'unique finding category per submission',
            'disclosure':'AI-assisted synthetic labels; retrospective split, not independent held-out validation. Ambiguous cases excluded from precision/recall. Failures are reported separately.',
            'cases':[]}
    with httpx.Client(base_url=base,timeout=75) as client:
        health=client.get('/api/health');health.raise_for_status(); result['release']=health.json()
        if result['release'].get('release')!='round3-finish': raise RuntimeError('Round 3 release is not live yet')
        accounts=client.get('/api/demo-accounts').json()['accounts']
        creator=next(x for x in accounts if x['role']=='creator')
        login=client.post('/api/login',json={'email':creator['email'],'password':creator['password']});login.raise_for_status()
        client.headers['Authorization']='Bearer '+login.json()['token']
        try:
            result['configuration']=client.get('/api/me').json()
            for case in fixture['cases']:
                started=time.monotonic()
                row={'id':case['id'],'group':case['group'],'split':case['split'],
                     'expected':sorted({x['category'] for x in case['expected']})}
                try:
                    body={'title':'Evaluation '+case['id'],'text':case['text'],'purpose':case['purpose'],'audience':case['audience'],'channel':'social','ai_consent':True,
                          'request_id':'r3-eval-'+result['release']['commit']+'-'+case['id']}
                    response=client.post('/api/submissions',json=body);response.raise_for_status();sub=response.json()
                    response=client.post(f"/api/revisions/{sub['latest_revision']}/review",json={});response.raise_for_status();review=response.json()
                    row.update(submission_id=sub['id'],revision_id=sub['latest_revision'],review_id=review['id'],status=review['status'],checks=review['checks'],model=review['model'],predicted=sorted({x['category'] for x in review['findings']}),findings=review['findings'],error=review['error'])
                except Exception as exc:
                    row.update(status='failed',predicted=[],error=type(exc).__name__)
                row['seconds']=round(time.monotonic()-started,2);result['cases'].append(row)
                Path(output).write_text(json.dumps(result,indent=2)+'\n')
                print(case['id'],row['status'],row['predicted'],flush=True)
        finally:
            client.post('/api/logout',json={})
    counts=defaultdict(lambda:dict(tp=0,fp=0,fn=0))
    for c in result['cases']:
        if c['group']=='ambiguous': continue
        expected=set(c['expected']); predicted=set(c['predicted']) if c['status']=='complete' else set()
        for x in expected&predicted:counts[x]['tp']+=1
        for x in predicted-expected:counts[x]['fp']+=1
        for x in expected-predicted:counts[x]['fn']+=1
    def metrics(c):return {**c,'precision':c['tp']/(c['tp']+c['fp']) if c['tp']+c['fp'] else None,'recall':c['tp']/(c['tp']+c['fn']) if c['tp']+c['fn'] else None}
    total={k:sum(c[k] for c in counts.values()) for k in ('tp','fp','fn')}
    result.update(finished_at=datetime.now(timezone.utc).isoformat(),categories={k:metrics(v) for k,v in counts.items()},overall=metrics(total),complete=sum(c['status']=='complete' for c in result['cases']),incomplete=sum(c['status']!='complete' for c in result['cases']),control_false_alarms=sum(bool(c['predicted']) and c['status']=='complete' for c in result['cases'] if c['group']=='compliant'))
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['overall','complete','incomplete','control_false_alarms']}),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--url',required=True);p.add_argument('--output',required=True);p.add_argument('--consent-synthetic-ai',action='store_true');a=p.parse_args()
    if not a.consent_synthetic_ai:p.error('Pass --consent-synthetic-ai to send the fictional fixture through the configured live provider')
    run(a.url,a.output)

"""Verify a public synthetic demo; no source changes or external messages."""
import json, uuid
from datetime import datetime, timezone
from pathlib import Path
import httpx

out={'checked_at':datetime.now(timezone.utc).isoformat(),'checks':{}}
tokens={}
with httpx.Client(base_url='https://brandproof.onrender.com',timeout=75) as c:
    def req(path,body=None,role='creator',expected=200):
        headers={'Authorization':'Bearer '+tokens[role]} if role in tokens else {}
        r=c.get(path,headers=headers) if body is None else c.post(path,json=body,headers=headers)
        assert r.status_code==expected,(path,r.status_code,r.text[:200])
        return r.json()
    def check(name,value=True):
        out['checks'][name]=value
        Path('docs/live-release-check.json').write_text(json.dumps(out,indent=2)+'\n')
        print(name,value,flush=True)
    try:
        out['health']=req('/api/health')
        for a in req('/api/demo-accounts')['accounts']:
            tokens[a['role']]=req('/api/login',{'email':a['email'],'password':a['password']})['token']
        check('three_demo_logins')
        body=dict(title='Final release verification '+uuid.uuid4().hex[:6],purpose='Announce Northstar One',audience='Customers',channel='social',text='Enjoy 20 hours of battery life.',ai_consent=True,request_id=uuid.uuid4().hex)
        sub=req('/api/submissions',body);out['submission_id']=sub['id']
        check('duplicate_save_returns_same_submission',req('/api/submissions',body)['id']==sub['id'])
        req('/api/submissions',{**body,'title':' '},expected=422);check('blank_input_rejected')
        run=req(f"/api/revisions/{sub['latest_revision']}/review",{})
        assert run['status']=='complete',run.get('error')
        check('live_ai_review_complete');out['model']=run['model']
        check('ranked_evidence_visible',bool(run.get('retrieval')))
        idx=next(i for i,f in enumerate(run['findings']) if f['category']=='contradiction' and f['quote']=='20 hours')
        f=run['findings'][idx]
        edit=dict(review_id=run['id'],revision_id=sub['latest_revision'],index=idx,start=body['text'].index(f['quote']),replacement=f['suggestion'],reason='Synthetic release check: preserve approved qualifier.')
        preview=req('/api/corrections/preview',edit)
        assert 'up to 12 hours' in preview['after']
        rev=req('/api/corrections/apply',edit)
        check('exact_correction_creates_new_revision',rev['id']!=sub['latest_revision'])
        req('/api/corrections/apply',edit,expected=409);check('duplicate_stale_correction_rejected')
        run=req(f"/api/revisions/{rev['id']}/review",{})
        assert run['status']=='complete' and not any(f['severity']=='high' for f in run['findings'])
        b={'revision_id':rev['id']};path=f"/api/submissions/{sub['id']}"
        req(path+'/request-approval',b);req(path+'/request-approval',b);check('repeat_approval_request_safe')
        req(path+'/approve',{**b,'action':'approved','reason':'Verified synthetic copy against approved battery source.'},role='reviewer')
        check('separate_reviewer_approval',req(path)['status']=='approved')
        evidence=req(path+'/evidence',role='reviewer');check('approval_evidence_available',bool(evidence['approvals']))
        req(path+'/revisions',{**body,'text':preview['after']+' Discover Northstar One today.','expected_revision_id':rev['id']})
        detail=req(path);check('edit_invalidates_approval',detail['status']=='draft' and bool(detail['approvals']))
        req('/api/notifications',role='reviewer');check('reviewer_inbox_accessible')
        out['passed']=all(out['checks'].values())
    except Exception as e:
        out['passed']=False;out['error']=str(e);print(type(e).__name__,str(e),flush=True)
    finally:
        for role in tokens:
            try:req('/api/logout',{},role)
            except Exception:pass
        Path('docs/live-release-check.json').write_text(json.dumps(out,indent=2)+'\n')
if not out['passed']:raise SystemExit(1)

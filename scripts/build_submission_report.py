from pathlib import Path
import json,math,sys
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
ROOT=Path(__file__).resolve().parents[1];R=ROOT;O=ROOT/'output/pdf/BrandProof_Round_3_Final.pdf';O.parent.mkdir(parents=True,exist_ok=True)
e=json.loads((R/'docs/evaluation-ai-improved.json').read_text())
if '--proof' in sys.argv:
 O=ROOT/'tmp/layout-proof.pdf'
 if 'overall' not in e:
  tp=fp=fn=0
  for z in e['cases']:
   if z['group']=='ambiguous':continue
   expected=set(z['expected']);pred=set(z['predicted']) if z['status']=='complete' else set()
   tp+=len(expected&pred);fp+=len(pred-expected);fn+=len(expected-pred)
  e.update(overall={'precision':tp/max(tp+fp,1),'recall':tp/max(tp+fn,1)},complete=sum(x['status']=='complete' for x in e['cases']),incomplete=sum(x['status']!='complete' for x in e['cases']),control_false_alarms=sum(bool(x['predicted']) for x in e['cases'] if x['group']=='compliant'))
else: assert 'overall' in e
quality=json.loads((R/'docs/correction-quality-assessment.json').read_text());assert quality['refined_live_check']['passed']
live=json.loads((R/'docs/live-release-check.json').read_text());assert live['passed']
for name,file in [('D','DejaVuSans.ttf'),('DB','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
pdfmetrics.registerFontFamily('D',normal='D',bold='DB',italic='D',boldItalic='DB')
W,H=842,595;M=42;G='#143F35';L='#D0EE91';BG='#F7F5EE';INK='#18372F';MUT='#61756B';LINE='#D8DFD5';PALE='#E8EEE2';ORANGE='#BD663D'
c=canvas.Canvas(str(O),pagesize=(W,H));c.setTitle('BrandProof | Final Product Dossier | Round 3');c.setAuthor('Team RAKSHITA7050');page_num=0
pct=lambda v:f'{100*v:.1f}%'
url='https://brandproof.onrender.com/';repo='https://github.com/SinghhSarvesh/brandproof'
def rect(x,y,w,h,fill,r=0,stroke=None):
 c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor(stroke or fill))
 c.roundRect(x,H-y-h,w,h,r,fill=1,stroke=bool(stroke)) if r else c.rect(x,H-y-h,w,h,fill=1,stroke=bool(stroke))
def text(t,x,y,size=11,color=INK,bold=False):
 c.setFillColor(HexColor(color));c.setFont('DB' if bold else 'D',size);c.drawString(x,H-y-size,t)
def para(t,x,y,w,size=10,color=INK,bold=False,maxh=None):
 style=ParagraphStyle('p',fontName='DB' if bold else 'D',fontSize=size,leading=size*1.43,textColor=HexColor(color))
 p=Paragraph(t,style);ww,hh=p.wrap(w,1000)
 if maxh is not None:assert hh<=maxh,(t[:45],hh,maxh)
 assert y+hh<H-28,(t[:45],y+hh)
 p.drawOn(c,x,H-y-hh);return hh

def rule(y,x=M,w=W-2*M,color=LINE):
 c.setStrokeColor(HexColor(color));c.setLineWidth(.7);c.line(x,H-y,x+w,H-y)
def tag(t,x,y,dark=False):
 w=pdfmetrics.stringWidth(t,'DB',8)+18;rect(x,y,w,21,L if dark else PALE,5);text(t,x+9,y+5,8,G,True)
def header(k,t,sub=None):
 global page_num
 page_num+=1;rect(0,0,W,H,BG);text('BrandProof',M,24,13,G,True);text('FINAL PRODUCT DOSSIER / TECHCIRCUIT',W-300,28,8,MUT);rule(54)
 text(k.upper(),M,75,9,MUT,True);text(t,M,94,min(28,758/max(pdfmetrics.stringWidth(t,'DB',28),1)*28),G,True)
 if sub:para(sub,M,138,740,10,MUT)
def footer():
 rule(557);text('RAKSHITA7050  /  30 OCTOBER 2026',M,567,7,MUT);text(f'{page_num:02d}',W-M-15,564,10,G,True);c.showPage()
def card(x,y,w,h,title,body,n=None):
 rect(x,y,w,h,'#FFFFFF',10);yy=y+18
 if n:text(n,x+18,yy,9,MUT,True);yy+=22
 para(title,x+18,yy,w-36,14,G,True);para(body,x+18,yy+43,w-36,9.7,MUT,maxh=h-(yy-y)-53)
def link(label,target,x,y,w=650,size=9):
 h=para(label,x,y,w,size,G);c.linkURL(target,(x,H-y-h,x+w,H-y),relative=0,thickness=0)
def arrow(x1,y1,x2,y2,color=MUT):
 c.setStrokeColor(HexColor(color));c.setFillColor(HexColor(color));c.setLineWidth(1.4);c.line(x1,H-y1,x2,H-y2)
 a=math.atan2(y2-y1,x2-x1);p=c.beginPath();p.moveTo(x2,H-y2)
 for off in (-.5,.5):p.lineTo(x2-7*math.cos(a+off),H-(y2-7*math.sin(a+off)))
 p.close();c.drawPath(p,fill=1,stroke=0)
def qrcode(target,x,y,size=64):
 q=qr.QrCodeWidget(target);b=q.getBounds();d=Drawing(size,size,transform=[size/(b[2]-b[0]),0,0,size/(b[3]-b[1]),0,0]);d.add(q);renderPDF.draw(d,c,x,H-y-size)
# 1 - cover
page_num=1;rect(0,0,W,H,G);rect(535,0,307,H,'#204D40');text('TECHCIRCUIT 2026  /  INKLOOM AI CHALLENGE',M,33,9,L,True)
text('BrandProof',M,92,46,'#FFFFFF',True)
para('Create freely.<br/>Approve with evidence.',M,168,470,29,'#FFFFFF',True)
para('A pre-publication workspace that connects approved brand sources, precise corrections and accountable human decisions.',M,268,440,12,'#D5E4D7')
tag('ROUND 3 / THE FINISH',M,356,True)
para('Team RAKSHITA7050<br/><b>Rakshita Jha</b> · Karunasankar M · Sarvesh Singh',M,395,460,10,'#FFFFFF')
for i,(a,b) in enumerate([('01  EVIDENCE','What supports this finding?'),('02  CORRECTION','What exactly will change?'),('03  APPROVAL','Which revision was approved?')]):
 y=104+i*112;rect(566,y,234,87,'#F7F5EE',10);text(a,582,y+15,10,G,True);para(b,582,y+39,199,13,G,True)
rect(M,487,758,66,L,9);para('<b>Try the product</b><br/>brandproof.onrender.com',M+16,500,290,10,G);c.linkURL(url,(M,42,M+310,108),relative=0)
para('<b>Public source</b><br/>github.com/SinghhSarvesh/brandproof',M+334,500,340,10,G);c.linkURL(repo,(M+330,42,740,108),relative=0);qrcode(url,730,490,60)
c.showPage()
# 2
header('01 / Problem, users and value','Good content can still use the wrong facts.','BrandProof sits between content creation and publication. It keeps people responsible for the final decision.')
card(M,185,239,164,'The creator','Drafts campaign copy and needs a clear explanation of what conflicts with approved evidence.','CREATE')
card(301,185,239,164,'The reviewer','Needs the exact revision, supporting sources and an explicit reason before approving.','DECIDE')
card(560,185,240,164,'The manager','Maintains current brand evidence and sees which previous decisions need revalidation.','GOVERN')
rect(M,371,758,147,G,10)
text('BEFORE',62,391,9,L,True);para('Guidelines in separate files.<br/>Corrections without traceable evidence.<br/>Approval status detached from later edits.',62,418,310,11,'#FFFFFF')
arrow(398,441,438,441,L)
text('WITH BRANDPROOF',460,391,9,L,True);para('Ranked, versioned source citations.<br/>Previewed changes saved as new revisions.<br/>Approval bound to content and evidence.',460,418,316,11,'#FFFFFF')
footer()
# 3
header('02 / Main product journey','From a risky claim to an approved revision.','Illustrative workflow using the real Northstar demo content; the deployed API journey is independently recorded in the repository.')
rect(M,182,466,329,'#FFFFFF',12);tag('CREATOR / DRAFT',62,199);para('Enjoy <font color="#BD663D"><b>20 hours</b></font> of battery life.',62,240,423,19,G)
rule(287,62,423);text('APPROVED EVIDENCE',62,305,8,MUT,True);para('“Up to 12 hours of battery life.”',62,327,423,17,G,True);para('A versioned source supports the numeric finding. The creator can inspect its exact quotation before changing the copy.',62,365,418,10,MUT)
rect(62,425,426,65,PALE,8);text('PREVIEWED CORRECTION',77,437,8,MUT,True);para('Enjoy <b>up to 12 hours</b> of battery life.',77,458,394,13,G)
for i,(a,b) in enumerate([('1. Check','Consent to AI review. Inspect findings and their sources.'),('2. Correct','Preview the exact replacement. Save a new revision and rerun checks.'),('3. Decide','Switch to Reviewer. Record a decision reason and approve the current revision.'),('4. Keep it valid','Later edits return to draft. Relevant evidence changes require revalidation.')]):
 y=186+i*81;text(a,540,y,13,G,True);para(b,540,y+25,255,10,MUT)
footer()
#4
header('03 / Round 2 commitments','Three substantial extensions. One coherent workflow.','The original product direction is unchanged. Each addition closes a gap in evidence, correction or approval.')
rows=[('01','Evidence you can inspect','Filtered source lists','Ranked lexical evidence; visible citations and versions; validity handling; explicit same-attribute fact conflicts; 40 labelled cases and live measurement.','Measured against the original 85% precision / 80% recall target.'),('02','Corrections that preserve intent','Manual editing only','Before/after preview; editable exact-span replacements; accept/reject records; protected numbers, names and qualifiers; stale edits rejected; immutable revisions.','20 correction cases: automated outcomes plus a disclosed AI-assisted quality rubric.'),('03','Approval of the exact revision','Broad source invalidation','Source-specific impact tracking; revalidation inbox; persistent in-app alerts; approval evidence export; PostgreSQL race-condition tests.','Only relevant new-format approvals are invalidated. Expiry is detected on reads.')]
for i,(n,title,old,new,note) in enumerate(rows):
 y=184+i*116;rect(M,y,758,102,'#FFFFFF',9);text(n,58,y+17,25,G,True);para(title,110,y+14,218,13,G,True);para('ROUND 2: '+old,110,y+59,210,8.5,MUT)
 para(new,354,y+14,423,9.3,INK,maxh=48);para(note,354,y+70,423,8.2,MUT,maxh=25)
footer()
#5
header('04 / Evidence and measured improvement','Less noise. More useful review.','Same 40-case benchmark and labels. Earlier results are preserved; this is a regression evaluation, not a blind holdout.')
pr=e['overall']['precision'];rc=e['overall']['recall'];met=pr>=.85 and rc>=.8
for x,label,old,new,target in [(M,'PRECISION',.5757575758,pr,.85),(430,'RECALL',.95,rc,.8)]:
 rect(x,181,370,135,G,10);text(label,x+18,196,9,L,True);text(pct(new),x+18,220,35,'#FFFFFF',True);para('Previous '+pct(old)+'  /  Target '+pct(target),x+18,272,330,10,'#D5E4D7');rect(x+165,240,181,9,'#4E6A5D',4);rect(x+165,240,181*new,9,L,4)
tag('BOTH THRESHOLDS MET' if met else 'TARGET SHORTFALL DISCLOSED',M,333)
para(f"<b>{e['complete']}/40</b> reviews complete · <b>{e['incomplete']}</b> incomplete · <b>{e['control_false_alarms']}/10</b> compliant controls flagged",M,372,758,12,G)
para('Six ambiguous cases hit provider rate limits; all 30 scored cases completed.',M,396,758,8.3,MUT)
rect(M,413,365,107,'#FFFFFF',9);text('HOW THIS WAS SCORED',58,428,9,G,True);para('10 compliant + 20 clear-issue cases are scored by unique finding category. Ten ambiguous cases remain visible but are excluded. Incomplete reviews count expected issues as misses.',58,450,332,9.3,MUT)
rect(430,413,370,107,'#FFFFFF',9);text('WHAT THE RESULT DOES NOT CLAIM',446,428,9,G,True);para('Combined rules + Groq review, not model-only accuracy. Synthetic AI-assisted labels and a retrospective split limit generalisation. No customer accuracy, blind study or human validation is claimed.',446,450,336,9.3,MUT)
footer()
#6
header('05 / Correction and reliability evidence','Control is tested at the points that matter.','Application CI and live checks cover the main journey, repeated actions and stale state.')
for x,n,label in [(M,'67','PostgreSQL tests passed'),(302,'2','Browser journeys passed'),(562,'12','Live API checks passed')]:
 rect(x,182,238,104,PALE,10);text(n,x+18,196,33,G,True);para(label,x+18,249,207,10,G)
rect(M,308,366,218,'#FFFFFF',10);text('CORRECTION QUALITY',60,325,10,G,True);text('18 edits + 2 safe rejections',60,351,16,G,True)
para('The original 20 automated correction cases pass. A separate AI-assisted rubric checks intent, approved facts, new claims and grammatical completeness.',60,388,328,10,MUT)
para('One weak deletion was refined through the existing edit flow: <b>“Choose No. 1 today.” → “Choose the product today.”</b> The refined result was verified live. Independent human validation remains a separate future check.',60,444,328,9.4,MUT)
rect(430,308,370,218,G,10);text('GUARDS AGAINST STALE DECISIONS',448,326,10,L,True)
items=['Duplicate corrections: one edit, then stale rejection.','Concurrent decisions: one valid transition.','Edit versus approval: new text cannot inherit approval.','Source change versus approval: current evidence wins.','Incomplete review: approval remains blocked.']
for i,t in enumerate(items):para('• '+t,448,360+i*29,333,9.6,'#FFFFFF')
footer()
#7
header('06 / Technical architecture','A small system with explicit trust boundaries.','React and FastAPI share one deployment. PostgreSQL persists the evidence behind every decision.')
boxes=[(M,187,220,72,'ROLE-AWARE CLIENT','React 19 · TypeScript · Vite'),(311,187,220,72,'WORKFLOW API','FastAPI · Pydantic · sessions'),(580,187,220,72,'DURABLE RECORDS','SQLAlchemy · PostgreSQL')]
for x,y,w,h,a,b in boxes:rect(x,y,w,h,G,9);text(a,x+14,y+14,9,L,True);para(b,x+14,y+37,w-28,10,'#FFFFFF')
arrow(264,223,307,223);arrow(533,223,576,223)
rect(311,299,220,88,PALE,9);text('REVIEW ENGINE',325,314,10,G,True);para('Rules + lexical retrieval<br/>Exact source / quote validation',325,339,195,9.5,G)
rect(580,299,220,88,'#FFFFFF',9);text('HOSTED SEMANTIC REVIEW',594,314,9,G,True);para('Groq · openai/gpt-oss-20b<br/>Explicit consent · no publishing tool',594,339,195,9.2,MUT)
arrow(421,263,421,295);arrow(535,343,576,343);text('selected sources + draft',546,280,7,MUT)
rect(M,299,220,88,'#FFFFFF',9);text('BOUNDED EXTRACTION',56,315,9,G,True);para('pypdf · Pillow · Tesseract<br/>Original file bytes discarded',56,340,193,9.4,MUT);arrow(265,343,307,343)
rule(414)
para('<b>Stored:</b> users, sessions, sources, submissions, immutable revisions, reviews, comments, decisions, approvals, notifications and audit events.',M,435,359,10,INK)
para('<b>Delivery:</b> multi-stage Docker image on Render; GitHub Actions runs SQLite/PostgreSQL tests, frontend build and Playwright. README includes local and Docker setup.',440,435,359,10,INK)
para('Local setup and complete feature inventory: README.md. Uploads: 5 MB / 20 PDF pages; drafts: 2,000 words / 20,000 characters; images: 16 MP. Typed JSON records trade database foreign keys for prototype speed.',M,510,758,9,MUT)
footer()
#8
header('07 / Responsible design and honest limits','Human decisions. Visible evidence. Bounded automation.','Security and accessibility controls are implemented; certification and production readiness are not claimed.')
card(M,183,239,183,'Privacy','Shared fictional demo. Per-revision consent before AI transmission. Provider keys stay server-side. Extracted text persists; original upload bytes are discarded.','MINIMISE EXPOSURE')
card(301,183,239,183,'Security','Salted scrypt hashes, hashed expiring sessions, logout revocation, server-side organisation and role checks, input limits and transaction locks.','ENFORCE BOUNDARIES')
card(560,183,240,183,'Accessibility','Labelled controls, native buttons, visible focus, textual status and responsive layouts. Browser checks cover mobile fit; no WCAG or screen-reader certification.','KEEP IT USABLE')
rect(M,389,758,136,G,10);text('KNOWN LIMITS / NEXT PRIORITIES',60,406,10,L,True)
para('<b>Product:</b> lexical retrieval can miss paraphrases; conflict detection uses shared attribute keys. Image and logo checks are narrow. Scanned PDFs are unsupported. In-app alerts are durable, but there is no email/push or background expiry scheduler.',60,435,350,9.5,'#FFFFFF')
para('<b>Operations:</b> free-host cold starts and provider limits; shared demo accounts; no SSO, RLS, production rate limiting or retention workflow. Next: isolated pilots, blind evaluation, human assessment, migrations, backups and bounded jobs.',438,435,344,9.5,'#FFFFFF')
footer()
#9
header('08 / Team, provenance and submission','Built on the proposal. Finished with evidence.','Team RAKSHITA7050 · TechCircuit · Inkloom AI problem statement')
rect(M,180,360,172,'#FFFFFF',10);text('TEAM-REPORTED CONTRIBUTIONS',60,197,9,G,True)
for i,(a,b) in enumerate([('Rakshita Jha / Team leader','Requirements, user validation, submission coordination'),('Karunasankar M','Frontend and review interfaces'),('Sarvesh Singh','Backend, AI review and data access')]):
 y=224+i*40;text(a,60,y,10,G,True);para(b,60,y+17,323,8.5,MUT)
rect(424,180,376,172,PALE,10);text('BUILD HISTORY & REQUIRED DISCLOSURE',442,197,9,G,True)
para('Round 2 baseline: <b>7a1aceb / 23 Oct</b>.<br/>Round 3 features: <b>29 Oct</b>.<br/>Review-policy improvements and verification: <b>30 Oct</b>. Earlier work is disclosed separately; history is not rewritten.',442,225,339,9.3,G)
para('ChatGPT/Codex significantly assisted implementation, fixtures, tests and documentation. The team remains responsible for review and explanation. Open-source dependencies and hosted APIs are recorded in the repository.',442,291,339,8.5,MUT)
text('VERIFY THE WORK',M,377,10,G,True)
for i,(label,path) in enumerate([('Working product',url),('Public source and local setup',repo),('Measured results and raw evidence',repo+'/blob/main/docs/FINAL_EVIDENCE.md'),('Copy-paste submission answers',repo+'/blob/main/docs/FINAL_FORM_ANSWERS.md')]):link(label,path,M,403+i*25,350,10)
rect(424,378,376,147,G,10);text('FINAL TEAM ACTIONS',442,395,10,L,True)
para('Upload this PDF to Drive with public viewer access. Check every link in a private window. Confirm registration details and contributions. Rakshita submits once before the organiser’s 30 October, 11:59 PM deadline; confirm its timezone.',442,422,338,9.4,'#FFFFFF')
para('The specific final-round brief requires no video or social-media post. The organiser form has not been submitted.',442,493,338,8.2,'#D5E4D7')
footer();c.save();print(O)

# BrandProof — Round 3: The Finish

Evidence-led brand review with controlled corrections and approval of an exact revision.

**[Open the working product](https://brandproof.onrender.com/)** · **[Source repository](https://github.com/SinghhSarvesh/brandproof)** · Team **RAKSHITA7050**, TechCircuit / Inkloom AI problem statement.

## Try it as a judge

The free service may take a short time to wake up. Choose **Creator** under Quick Demo Fill and select **Open workspace**. These are public, shared synthetic demo accounts: never enter personal, confidential or real client content.

1. Choose **New review**. Title: `Northstar launch`. Purpose: `Announce Northstar One`. Draft: `India's No. 1 device. Enjoy 20 hours of battery life. Meet NS1.`
2. Consent to the displayed AI provider, save and **Run checks**. Inspect the source quotations and ranked evidence. Incomplete checks cannot be approved.
3. Open **Accept or edit correction**, inspect the replacement, **Preview exact change**, then **Accept and save new revision**. Each accepted edit requires fresh checks. You can also edit the whole draft to `Meet Northstar One. Enjoy up to 12 hours of battery life.`
4. Run checks and **Request approval**. Sign out; choose **Reviewer**. Open the awaiting-review item, inspect evidence, add a reason and approve. High-severity findings require an explicit exception reason.
5. Sign back in as Creator and edit the approved item: it returns to draft. As Manager, inspect Brand sources, Insights, Activity and the revalidation inbox. Superseding relevant evidence requires a fresh decision; unrelated evidence does not invalidate new-format approvals.

Demo identities: `creator@brandproof.demo`, `reviewer@brandproof.demo`, `manager@brandproof.demo`. Quick Demo Fill supplies public demo credentials. No social post or video submission is required by the supplied final-round brief.

## Built features

- Role and organisation checks; salted password hashes, expiring sessions and logout revocation.
- Versioned facts, terms, tone, claims, dimensions and standalone-logo hashes, scoped by channel and validity dates.
- Text/PDF submissions, PNG/JPEG extraction, OCR, image dimensions, logo hash comparison and alt-text presence checks.
- Ranked lexical evidence with structured-rule precedence, versioned citations and explicit conflicting-fact warnings.
- Deterministic checks plus a hosted semantic-review adapter; consent, bounded provider timeout and validation of exact draft/source quotes.
- Exact-span correction preview, editable replacements, accept/reject actions, numeric/name/qualifier safeguards and immutable revisions.
- Review requests, high-severity exceptions, self-approval prevention, revision history and inspectable approval evidence.
- Relevant-source revalidation, durable in-app notifications with per-user read state, insights and application audit events.
- Empty-input rejection, duplicate initial-save keys, repeat-review reuse, repeat approval-request safety, stale-edit rejection, refresh recovery and visible failure states.

## Run locally — Python 3.12 and Node 22

Linux/macOS:

```sh
git clone https://github.com/SinghhSarvesh/brandproof.git
cd brandproof
python3 -m venv .venv
. .venv/bin/activate
pip install -r backend/requirements.txt
export DEMO_PASSWORD='local-synthetic-demo-password'
export DEMO_QUICK_FILL=true
export REVIEW_MODE=rules_only
(cd backend && python seed.py)
(cd frontend && npm ci)
python scripts/dev.py
```

Windows PowerShell:

```powershell
git clone https://github.com/SinghhSarvesh/brandproof.git
cd brandproof
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
$env:DEMO_PASSWORD='local-synthetic-demo-password'
$env:DEMO_QUICK_FILL='true'
$env:REVIEW_MODE='rules_only'
cd backend
python seed.py
cd ../frontend
npm ci
cd ..
python scripts/dev.py
```

Open **http://localhost:4173**. SQLite is used locally unless `DATABASE_URL` is set. Install Tesseract and put it on PATH for image OCR; otherwise the UI correctly reports incomplete OCR. Hosted AI is optional for local setup; rules-only mode is visibly labelled and does not claim semantic coverage. Local Python does not auto-read `.env`.

## Docker and PostgreSQL

Install/start Docker. Copy `.env.example` to `.env` (`Copy-Item` on PowerShell), set unique `POSTGRES_PASSWORD` and `DEMO_PASSWORD`, then:

```sh
docker compose up --build -d
docker compose exec app python seed.py
```

Open **http://localhost:8000**. Stop with `docker compose down`. Avoid `-v` unless intentionally deleting the database volume. PostgreSQL passwords in Compose URLs should be URL-safe alphanumeric. Public Quick Demo Fill must remain disabled for private deployments. The Docker image includes Tesseract and serves the built UI with FastAPI.

## AI setup

Set backend-only environment variables: `REVIEW_MODE=ai`, `AI_PROVIDER_LABEL`, `AI_BASE_URL`, `AI_MODEL`, `AI_API_KEY`. The existing deployment uses Groq's compatible endpoint and `openai/gpt-oss-20b`; check live review records for the model actually used. Keep credentials in platform secrets, never source code or frontend variables. Only synthetic text, purpose, audience and selected sources are sent after consent. Provider failure or invalid evidence produces an incomplete review, not a clean result.

## Tests and evaluation

```sh
cd backend
python -m pytest tests -q
python evaluate.py --output ../docs/evaluation-rules.json
cd ../frontend
npm run build
```

GitHub Actions additionally provisions **PostgreSQL 16**, runs concurrency tests, builds the UI and runs Playwright browser journeys against an isolated synthetic app. CI publishes browser traces/screenshots and the evaluation report. See [Testing](docs/TESTING.md) for current evidence and limitations.

The 40-case synthetic fixture contains 10 controls, 20 clear issues and 10 ambiguous cases. The 20 correction pairs check exact edits and unsafe replacements. These fixtures are not independent customer validation or proof of general AI accuracy. Do not present rules-only scores as semantic scores.

## Documentation

- [Round 3 changes and limitations](docs/ROUND3.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Privacy, security, accessibility and responsible design](docs/RESPONSIBLE_DESIGN.md)
- [Testing and reproduction](docs/TESTING.md)
- [Participants and contributions](docs/CONTRIBUTIONS.md)
- [Submission checklist and roadmap](docs/SUBMISSION.md)

Render deploys this repository's `main` branch. No separate service is required. `/api/health` reports the release and deployment commit when available. Only call the release verified after the deployment is live and the main journey passes against it.

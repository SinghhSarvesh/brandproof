# BrandProof

Evidence-led brand content review with revision-specific human approval.

**TechCircuit · Round 2 · Team RAKSHITA7050**

A working prototype for reviewing campaign content against approved brand sources. This milestone covers the core review and approval workflow; see [implementation status](docs/STATUS.md) for tested capabilities and remaining work. Use synthetic materials while privacy controls are being completed.

## What works

- Separate creator, manager and reviewer accounts; server-side role and organisation checks.
- Approved fact, terminology, tone, claim, dimension and logo-hash source records, with versions, dates, scope and confirmation.
- Guideline PDF text import for manual rule definition and confirmation.
- Text submissions, immutable content revisions, comments and review history.
- Narrow deterministic numeric-claim, phrase, terminology, dimension, exact standalone-logo hash and alt-text metadata checks.
- Evidence-linked findings and manual correction editing. Rejection reasons are saved.
- Review requests, human approval, high-severity exception reasons, self-approval prevention and stale-revision rejection.
- Source snapshot changes mark existing approvals for revalidation.
- Text-PDF extraction and PNG/JPEG OCR, with explicit extraction failures.
- A hosted chat-completions AI adapter with consent, source/quotation validation and fail-closed results. Live provider integration is not yet verified.
- Insights based on stored findings and rejected findings, plus audit events.

The default `rules_only` mode is visibly labelled. It does **not** evaluate semantic tone or paraphrased claims. A rules-only approval records that limited review mode. Set `REVIEW_MODE=ai` only after configuring and validating the model provider. Failed AI review cannot proceed to approval.

## Run with Docker and PostgreSQL

Install Docker Desktop and start it. From the project directory:

```sh
cp .env.example .env
```

On Windows PowerShell use `Copy-Item .env.example .env` instead. Edit `.env` locally: set unique `POSTGRES_PASSWORD` and `DEMO_PASSWORD` values of at least 12 characters. Use URL-safe alphanumeric characters for the database password because Compose interpolates it into a database URL. Never commit `.env`.

```sh
docker compose up --build -d
docker compose exec app python seed.py
```

Open http://localhost:8000. Accounts are:

- `manager@brandproof.demo`
- `creator@brandproof.demo`
- `reviewer@brandproof.demo`

All initially use the locally configured `DEMO_PASSWORD`. Re-running the seed does not reset existing passwords. They are synthetic demonstration accounts, not production identities. Stop with `docker compose down`; the database volume is preserved. Do not add `-v` unless you intend to erase the demo database.

Docker/PostgreSQL configuration is provided but has not been executed in the build environment. The API tests used SQLite. Validate the PostgreSQL deployment before submission.

## Run without Docker

Python 3.12 and Node 22 or later are recommended. From the root on Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
$env:DEMO_PASSWORD = 'choose-a-local-demo-password'
cd backend
python seed.py
cd ..
cd frontend
npm ci
cd ..
python scripts/dev.py
```

On Linux/macOS:

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r backend/requirements.txt
export DEMO_PASSWORD='choose-a-local-demo-password'
(cd backend && python seed.py)
(cd frontend && npm ci)
python scripts/dev.py
```

Open http://localhost:4173. Development uses SQLite in `backend/brandproof.db` unless `DATABASE_URL` is set. Install Tesseract separately and put it on PATH to run image OCR; without it image reviews remain incomplete. Docker includes it. The `.env` file is consumed by Docker Compose, not automatically by the local Python process; set local environment variables explicitly.

## Verify

```sh
cd backend
python -m pytest tests -q
cd ../frontend
npm run build
```

The workflow tests cover success, invalidation, exceptions, role checks, tenant isolation, consent, missing/expired sources, invalid citations, review failures, idempotency, upload rejection, extraction and logout. See `docs/STATUS.md` for verified results and gaps.

## Demo in three accounts

1. Sign in as creator. Create a social post with purpose “Announce Northstar One” and text: `India’s No. 1 device. Enjoy 20 hours of battery life. Meet NS1.`
2. Save, then run checks. Inspect separate ranking, battery and naming findings and their source evidence.
3. Edit the draft to `Meet Northstar One. Enjoy up to 12 hours of battery life.` Save a new revision, rerun checks and request approval.
4. Sign out and sign in as reviewer. Open the content, write a decision reason and approve.
5. Sign in as creator and edit it again. The new revision is a draft requiring fresh review.
6. Sign in as manager. Inspect insights/activity and create a replacement battery source. Approvals associated with the earlier source snapshot require revalidation.

## AI configuration

Configure these variables on the backend only:

```text
REVIEW_MODE=ai
AI_PROVIDER_LABEL=<actual provider name>
AI_BASE_URL=<provider's supported chat-completions base URL>
AI_MODEL=<available model supporting JSON object responses>
AI_API_KEY=<secret from provider dashboard>
```

The adapter posts to `/chat/completions` using bearer authentication, a JSON object response format and temperature 0. Verify provider/model compatibility and retention terms before enabling. Only text, campaign purpose, audience and applicable active source passages are sent. Image pixels are not sent; OCR text currently receives deterministic checks only. Do not paste API keys into chat or put them in frontend variables. API call failures, malformed data or invalid citations produce incomplete reviews.

## Repository and deployment

Source repository: https://github.com/SinghhSarvesh/brandproof

A public deployment is not yet available.

The supplied Docker image serves the built React frontend and FastAPI on port 8000. Use a host that supports Python containers and PostgreSQL. Add HTTPS, platform secrets, database backups and ingress rate limits before exposing a judge deployment. Keep it synthetic-only until privacy controls are completed.

## Project records

- [Architecture](docs/ARCHITECTURE.md)
- [Implementation status and remaining work](docs/STATUS.md)
- [Contributions](docs/CONTRIBUTIONS.md)
- [Tool and AI assistance disclosure](docs/DISCLOSURES.md)

Evaluation targets are documented separately from measured results. Preserve real commit history during the official build window.

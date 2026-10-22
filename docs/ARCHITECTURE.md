# Architecture

The React client calls a same-origin FastAPI API. Development Vite proxies `/api` to port 8000; the Docker image serves the compiled client directly. PostgreSQL is the intended hosted database, with SQLite for development tests.

## Review pipeline

Authenticate session → validate organisation and revision ownership → snapshot applicable active sources → run exact checks → optionally invoke hosted model → validate output schema and citation/quotation membership → persist run and findings → allow revision-specific human decision.

Source IDs and quoted passages are checked in code. This proves that evidence exists in the authorised set, not that the model interpreted it correctly. Reviewers remain responsible for decisions. AI outputs never trigger publication or approval tools.

## Persistent records

Users and sessions use dedicated SQLAlchemy tables. Other prototype entities are stored in a tenant-indexed `records` table with `kind` and JSON payload: source, submission, revision, attachment metadata, review, comment, approval, decision and audit. IDs are server-assigned. Public routes offer no revision-update endpoint: content edits create new records.

This speeds the first milestone but sacrifices database foreign-key enforcement for those relationships. Migrations and normalised tables remain planned. Access control is applied before record retrieval. Source mutations and review decisions use an organisation advisory transaction lock on PostgreSQL. Submission mutation uses row locking. Test their concurrent behavior on PostgreSQL before judging.

## AI boundary

The provider adapter sends only draft text, purpose, audience and scoped approved sources. The JSON response has typed categories, severities and citations. Inputs are treated as untrusted data in the system instruction; the model has no tools. A request times out after 25 seconds of network inactivity. Failures return incomplete reviews. Prompt injection resilience has not yet been evaluated against a comprehensive adversarial corpus.

## Limits and operations

2,000 words / 20,000 characters per draft, 20 PDF pages, 5 MB per upload, 16 megapixels per image, 15-second OCR timeout, 45,000-character source budget in AI mode. The UI requests Google Fonts; remove or self-host for private production use. Serve behind HTTPS and platform-level rate limiting. Neither retention deletion nor external-provider retention assurances are complete.

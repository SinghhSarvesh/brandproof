# Round 3 form answers

## Hackathon / team / leader
TechCircuit
RAKSHITA7050
Rakshita Jha
Leader email: use the original registration email; not supplied here.
Members: Rakshita Jha, Karunasankar M, Sarvesh Singh.

## Working product
https://brandproof.onrender.com/

## Public source repository
https://github.com/SinghhSarvesh/brandproof

## Final PDF
Upload BrandProof_Round_3_Final.pdf to Google Drive and insert your Anyone with the link / Viewer URL. No Drive link is invented.

## Complete list of built features
Public Manager, Creator and Reviewer Quick Demo Fill sign-in.
Role, ownership and organisation enforcement with expiring sessions and logout.
Versioned approved source management with scope, validity dates and replacement history.
Campaign drafts and immutable revision history.
Text-PDF extraction and narrow image/OCR/metadata checks.
Deterministic terminology, claim and numeric checks.
Consented Groq semantic review with exact source and quotation validation.
Ranked lexical evidence, versioned citations and same-key fact-conflict warnings.
Exact-span correction preview and editable replacements.
Accept/reject records, numeric/name/qualifier safeguards and stale-edit rejection.
Revision-specific reviewer decisions, comments, reasons and high-severity exceptions.
Self-approval prevention and incomplete/stale review blocking.
Relevant-source revalidation and durable in-app notifications with read state.
Inspectable approval evidence and historical decisions.
Insights, audit activity, duplicate-action guards, refresh recovery and visible error states.

## Technical architecture and implementation summary
React 19, TypeScript and Vite provide the frontend. Python, FastAPI and Pydantic implement the API; SQLAlchemy and PostgreSQL persist users, sessions and organisation-scoped typed JSON records. A multi-stage Docker image serves the UI and API on Render. GitHub Actions runs SQLite/PostgreSQL tests, frontend builds and Playwright journeys.

The review engine combines deterministic checks with BM25-style lexical evidence ranking and Groq's openai/gpt-oss-20b adapter. Consent is required before draft and source text are sent. Source IDs, source evidence and draft quotations are validated; failed or conflicting reviews block approval. Controlled corrections create new revisions, and PostgreSQL locks protect revisions, corrections, source changes and reviewer decisions. pypdf, Pillow and Tesseract handle bounded extraction.

## Improvements after Round 2
1. Ranked evidence, visible citations/version/expiry handling, conflict warnings and a reproducible 40-case live evaluation are delivered. Precision 95.2% and recall 100.0% on the unchanged 40-case fixture (30 unambiguous cases scored). 34/40 reviews completed; 6 incomplete; 0/10 compliant controls flagged. The 85% precision / 80% recall thresholds are met on the disclosed combined-system fixture; this is not blind or general model validation.
2. Controlled corrections provide exact before/after previews, editable replacements, accept/reject actions, safeguards and stale-edit rejection. Twenty automated pairs pass (18 accepted edits, two rejections). A documented AI-assisted rubric, with one explicitly refined creator edit, assesses 18 intent-preserving proposals and two unsafe rejections; independent human assessment is not claimed.
3. Relevant-source approval tracking, a revalidation inbox, durable in-app alerts and evidence export are delivered. Four PostgreSQL concurrency tests pass. Alerts are not email/push and expiry is detected on reads.

## Testing details
Application CI: 67 PostgreSQL tests passed; SQLite 63 passed with four database-specific skips; frontend build passed; two Playwright tests passed. The live 4503217 release passed 12 API checks including correction-to-approval-to-edit invalidation. Public login visually inspected. Precision 95.2% and recall 100.0% on the unchanged 40-case fixture (30 unambiguous cases scored). 34/40 reviews completed; 6 incomplete; 0/10 compliant controls flagged. Fixtures are synthetic/AI-assisted, not independent customer validation. Ambiguous cases are reported separately. No load-test, WCAG or security certification is claimed.

## Privacy, security, accessibility and responsible design
Shared fictional demo: use no private client material. Originals are discarded after extraction; extracted text and workflow records persist. AI transmission requires consent and provider keys remain server-side. Salted scrypt hashes, hashed expiring sessions, server-side scope/role checks, bounded input and PostgreSQL locking protect the workflow. Labels, keyboard focus, textual statuses and responsive layout support basic accessibility; full accessibility certification is not claimed. AI cannot publish or approve. Human review remains mandatory. Production retention, onboarding, RLS, rate limiting and independent security review remain future work.

## Known limitations and roadmap
Hosted AI can produce false positives or incomplete reviews. Lexical ranking can miss paraphrases; conflict detection is limited to shared keys. Independent human intent assessment remains future validation. Public shared demo, free-host cold starts, no scanned-PDF support, narrow OCR/logo checks, no private original-file storage, no external alerts, queues, SSO, RLS, migration framework or production rate limits.

Next: independent intent assessment, broader blind evaluation, consented user walkthroughs and isolated pilot accounts. Then retention/deletion controls, rate limiting, migrations, backup/restore drills and bounded background review jobs. Later consider richer conflict semantics, paraphrase retrieval, SSO/RLS and wider visual analysis. No unmeasured time savings, revenue or guaranteed accuracy is claimed.

## Participant contributions and disclosure
Rakshita Jha: requirements, user validation and submission coordination. Karunasankar M: frontend and review interfaces. Sarvesh Singh: backend, AI review and data access. These are team-reported contributions, not an attribution audit. Supply any required institutional and registration fields separately.

ChatGPT/Codex significantly assisted implementation, fixtures, tests, debugging and documentation. The Round 2 baseline (7a1aceb, 23 October) is reused earlier work; it is not represented as newly built in Round 3. The main Round 3 commits were recorded on 29 October, with final verification on 30 October. Open-source dependencies and hosted APIs are listed in the repository. The team must review and explain all submitted work.

## Final confirmation
Only the team leader submits once. Confirm original registration details, organiser timezone and public access to all links. No video or social-media post is required by the specific Round 3 brief. Do not mark declarations complete before checking them yourself.

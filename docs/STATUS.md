> Historical Round 2 milestone. See [ROUND3.md](ROUND3.md) for the current changes and limitations.

# First implementation milestone

Built 22 October 2026. This document describes implementation status, not a final Round 2 submission.

## Verified in the development environment

- React/TypeScript production compilation succeeds.
- All 15 backend tests pass against an isolated SQLite database (18.25 seconds in the final run). One dependency deprecation warning is recorded; no test failures.
- Browser visual inspection confirms the login screen renders correctly at desktop size. Authenticated browser flows and mobile layout have not yet been manually verified; their backend workflows are covered by API tests.
- No live AI API call, container build, PostgreSQL integration or public deployment has been verified.

## Differences from the Round 1 plan at this milestone

| Area | Implemented now | Remaining |
| --- | --- | --- |
| Source management | Manual rules and imported guideline text; confirmation and source replacement | Automated candidate-rule extraction and clearer conflict resolution |
| Retrieval | Tenant-, scope-, validity- and version-filtered source set with a prompt size cap | PostgreSQL full-text ranking; current cap fails closed instead of truncating evidence |
| Facts | Exact phrase and narrow numeric-unit rules; optional semantic adapter | Live model validation, broader fact normalisation and conflict tests |
| Corrections | Creator manually edits using suggestions; rejection reasons | Per-suggestion accept-and-apply UI with reliable text offsets and protected-fact evaluation |
| Workflow | Revision IDs, source snapshots, role checks, exception reasons | Notifications, source-specific impact selection, production concurrency validation |
| Files | Temporary in-memory file extraction, extracted text/metadata stored | Private original asset storage, file downloads and retention/deletion workflow |
| Images | Dimensions, OCR rules, standalone-logo hash, alt metadata | Region coordinates, semantic OCR review, richer visual checks |
| Database | SQLAlchemy tables with tenant-scoped JSON records; PostgreSQL Compose | Normalised entity tables, migrations, database-level isolation policies |
| Security | Hashed passwords and session tokens, expiring/revocable sessions, role checks | Login rate limiting, organisation onboarding, SSO, production threat review |
| Reliability | Bounded input sizes, explicit failures, sequential review idempotency | Budget limits, retries, queues, load tests, hostile-file isolation |
| Evaluation | Automated workflow/extraction tests | 40 labelled submissions, held-out evaluation, 20 correction pairs and three real or disclosed proxy walkthroughs |

The broad source snapshot conservatively invalidates approvals when any active source changes, including unrelated sources. This avoids silently retaining approval but can cause extra review. PostgreSQL advisory transaction locks serialize source changes and decisions within each organisation; this code path still requires PostgreSQL testing. SQLite is for local single-user development/testing, not concurrent public deployment.

Current idempotency avoids duplicate completed runs for the same revision/source snapshot/mode/model. It does not implement a production distributed queue. Audit records are append-only through exposed application routes; administrators can still modify the database. No tamper-proof claim is made.

Original images/PDF bytes are not saved. Extracted text and metadata remain in the database until an administrator handles deletion. Do not upload real confidential materials yet. The same demo password is used for all three synthetic accounts during initial setup; it is unsuitable as production account management.

## Preserve the three improvement commitments

1. Evidence you can inspect: validate reference IDs and exact evidence; evaluate semantic relevance separately and improve conflict/expiry handling.
2. Corrections that preserve intent: build controlled application of suggestions and evaluate at least 18 of 20 correction pairs without unsupported new claims.
3. Approval of the exact revision: complete source-change and exception scenarios, concurrency testing and demonstrable invalidation.

Do not report the Round 1 85% precision, 80% recall or 18/20 correction goals as achieved until measured. Seeded content and automated tests are not user-testing evidence.


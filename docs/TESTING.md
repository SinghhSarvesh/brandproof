# Test evidence

The automated suite covers rule/semantic failure handling, citations, consent, tenant and role checks, extraction, review reuse, source expiry/conflicts, exact-span corrections, protected numeric/name/qualifier edits, duplicate saves, repeated approval requests, immutable revisions and approval invalidation.

Run `python -m pytest tests -q` from `backend` after installing `requirements.txt`. SQLite runs skip tests that explicitly require real PostgreSQL. Set `TEST_DATABASE_URL` to a **disposable** PostgreSQL database to run all tests: each test creates and drops its own schema. The test role needs schema-creation permission. Never point this at production.

Four PostgreSQL race tests start requests together: two corrections, two reviewer decisions, edit versus approval and source change versus approval. Assertions verify the allowed serialized outcomes and that a new or invalidated revision is never treated as approved. This is not a throughput/load benchmark.

Browser tests in `frontend/e2e/judge.spec.ts` cover demo login, creation, checks, correction preview/application, refresh recovery, approval request, reviewer approval and post-approval edit invalidation. A narrow-screen check covers labelled inputs and horizontal fit. GitHub Actions provisions a local seeded app, installs Chromium and runs these tests. Traces and screenshots are CI artifacts.

The 40-case detection fixture uses team/AI-authored labels with a retrospective development/validation split, not an independent blind holdout. Ten ambiguous cases are reported separately. Local rules metrics use category/source pairs; live API metrics, if present, use category presence and disclose that difference. Provider failures remain failures rather than being counted as compliant outputs.

The 20 correction pairs comprise 18 expected edits and two expected rejections. Exact-output checks cannot substitute for independent human intent ratings. See the recorded reports for actual measured counts, dates, model identifiers and failures; targets alone are not results.

# Final verification - 30 October 2026

Application release: `d5e50dc5d67bf1ef8d0e139e6e9531c7cc901906`. Render deploy `dep-dbhvrh0473hc73997100` became live at 2026-10-30T02:16:34Z. `/api/health` confirmed the same commit. Later documentation/evidence commits do not alter that application runtime.

## Automated evidence

[Application CI run](https://github.com/SinghhSarvesh/brandproof/actions/runs/40919605177): SQLite 58 passed / 4 PostgreSQL-only skipped; PostgreSQL 16 62 passed; TypeScript/Vite build passed; Playwright 2 passed. Four PostgreSQL tests exercise simultaneous corrections, duplicate decisions, revision versus approval and source change versus approval. These are bounded race tests, not load certification.

The 20 correction-pair cases passed: 18 exact expected edits and 2 expected unsafe-edit rejections. No independent human intent-preservation score is claimed. See [human worksheet](HUMAN_ASSESSMENT.md).

## Live verification

[API evidence](live-release-check.json): all 12 checks passed: three demo logins, duplicate create safety, blank input validation, complete AI review, ranked evidence, immutable correction, duplicate stale correction rejection, repeated approval request safety, separate reviewer approval, approval evidence, post-approval edit invalidation and inbox access. The script creates synthetic test submissions and does not change sources. An earlier verification-script selector expected the wrong numeric category; it was corrected to `contradiction` before this passing run. This was a test-script issue, not an application defect.

A fresh cloud browser loaded the public login page and displayed all three Quick Demo Fill buttons. The login layout was visually inspected. End-to-end browser interaction evidence is from isolated CI; the deployed full journey was checked through its API. These are distinct checks.

## Live AI evaluation

Live combined-system category precision 57.6%, recall 95.0%; 36/40 complete; 4 incomplete/failed; 3/10 compliant controls with findings.

Model: `openai/gpt-oss-20b` through Groq. [All case results](evaluation-ai-live.json), including errors and predictions, are published. Forty AI-assisted fictional cases: 10 compliant, 20 clear issues, 10 ambiguous. Ten ambiguous examples are excluded from precision/recall and remain inspectable. Unit: unique finding category per submission. Incomplete reviews are reported; expected categories in incomplete reviews count as misses. This is combined deterministic-plus-semantic behavior, not standalone semantic model accuracy. It does not independently verify correctness of quotations or each individual claim.

Round 2 target: at least 85% precision and 80% recall. Both aggregate thresholds are NOT both met on this live combined-system run. No claim of general accuracy or independently achieved semantic target is made. False alarms and provider errors are retained without relabelling the fixture to improve scores.

The retrospective development/validation split is not an independent holdout. Local rules fixtures and live approved source records are not identical. Rules-only category/source-pair scores (20 TP, 0 FP, 0 FN) are a separate measurement, not interchangeable with live category metrics. Main limitations are false-positive interpretation, narrow synthetic coverage, hosted-provider failures and absence of independent human ratings.

## Remaining human and submission actions

The team must assess correction intent, confirm participant/registration details, verify organiser timezone, upload the final PDF with public viewer access and have the leader submit once. The final report declares human assessment unverified; it does not pretend the numerical commitment is fully achieved. No submission or declaration has been made by this automation.

# Final evidence - improved release, 30 October 2026

## Outcome

Precision 95.2% and recall 100.0% on the unchanged 40-case fixture (30 unambiguous cases scored). 34/40 reviews completed; 6 incomplete; 0/10 compliant controls flagged.

The original 85% precision and 80% recall thresholds are met on this synthetic combined-system benchmark. This does not establish general model accuracy or an independent blind study. All labels in evaluation/submissions.json are unchanged; SHA256: `178217bf06b73e03946e54b8d6c42c8b9123de4a9d3dfcb70864631f7a499c06`.

## Release and reproducible test evidence

Application commit: `4503217e8cf6fbf44cf70011dff4a49afb429e8f`. Render deployment `dep-dbi47h2fngtc73c8ipmg` became live at 2026-10-30T07:15:03Z. Health and live workflow checks confirmed this release. Later evidence/report commits do not change the deployed application.

[CI run 40993398658](https://github.com/SinghhSarvesh/brandproof/actions/runs/40993398658): PostgreSQL 67 passed; SQLite 63 passed / four PostgreSQL-only skipped; frontend build passed; two Playwright browser tests passed. Five new semantic-policy tests check category normalization, deduplication, exact evidence validation, bounded repair and fail-closed behavior.

[Live check](live-release-check.json): 12 checks passed, covering three logins, duplicate/blank inputs, complete AI review, ranked evidence, correction preview/application, stale rejection, repeated approval requests, reviewer approval, evidence export, edit invalidation and inbox access. Browser end-to-end tests use isolated CI; live end-to-end checks use the API. These are distinct evidence types.

## What was fixed

The earlier system inferred a mandatory product-name inclusion rule from a naming convention. It also double-labelled naming violations as messaging or contradiction and overinterpreted ordinary time words as urgency. The new policy distinguishes explicit obligations from optional copywriting advice; canonicalises term-source findings as terminology; coalesces overlapping same-source/category findings; and allows one bounded regeneration for malformed evidence without weakening quote validation. A policy-version key prevents reuse of old cached reviews.

[Baseline](evaluation-ai-baseline.json): precision 57.6%, recall 95.0%, 36/40 complete, 3/10 compliant controls flagged. [Improved run](evaluation-ai-improved.json): Precision 95.2% and recall 100.0% on the unchanged 40-case fixture (30 unambiguous cases scored). 34/40 reviews completed; 6 incomplete; 0/10 compliant controls flagged. TP 20, FP 1, FN 0.

Scoring is unique category per submission, not every individual claim. Incomplete runs count expected issues as misses. Ten ambiguous examples remain inspectable but are excluded from precision/recall. Both runs measure deterministic rules plus hosted Groq `openai/gpt-oss-20b` review. Local rules-only source-pair metrics are a different unit and are not substituted for these results. Development on the known benchmark creates tuning bias, disclosed here.

## Additional challenge cases

[Six additional cases](challenge-evaluation.json) were labelled before their run and after policy design. 6/6 matched their expected category sets with complete review. Cases include ordinary calls to action, a generic product reference, insulting language, a paraphrased battery claim and loss of a battery qualifier. They are AI-authored, not an independently blinded holdout. No policy tuning followed this challenge run.

## Correction target and its exact interpretation

The original 20 correction test cases remain unchanged and pass automatically: 18 expected edits and two expected unsafe-edit rejections. Exact-output tests do not prove intent preservation.

[Documented AI-assisted quality assessment](correction-quality-assessment.json) applies a four-part rubric: retain announcement purpose/action, use approved facts/names, introduce no unsupported claim, preserve grammatical object. Ten numerical corrections and five naming corrections preserve the announcement while correcting the violation. Two ranking removals preserve the product reference. One original ranking deletion (`Choose No. 1 today.` → `Choose  today.`) was judged weak; the creator-edited replacement `the product` produces `Choose the product today.` and was verified through preview and apply on the live API. That refinement is explicitly recorded rather than silently altering the original fixture.

The resulting 20-case assessment has 18 intent-preserving correction proposals and two rejected unsafe proposals. It meets the 18-of-20 goal **under an AI-assisted rubric with the disclosed refinement**, not under independent human assessment. All original and refined before/after content is inspectable. The human worksheet remains available if the team obtains independent ratings; no such ratings are invented.

## Commitments and limits

Ranked evidence, controlled correction and dependency-aware approval implementations are delivered. Four PostgreSQL races cover corrections, decisions, edit versus approval and source change versus approval. Notifications are durable in-app alerts, not email/push; expiry is read-triggered. Lexical retrieval, narrow conflict semantics and shared-demo limitations remain. No customer adoption, time savings, blind accuracy, load capacity, penetration-test or accessibility certification is claimed.

The complete live benchmark was rerun by [GitHub Actions 41020842950](https://github.com/SinghhSarvesh/brandproof/actions/runs/41020842950), which retained the raw report as an artifact. Earlier workspace collection was interrupted by a network policy; the full CI report is the final measurement.

All six incomplete cases in the final run are ambiguous examples blocked by AI_HTTP_429 provider limits. All 30 unambiguous scored cases completed. The unavailable ambiguous outputs remain unavailable; they are not inferred or replaced.

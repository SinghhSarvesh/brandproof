# Round 3 implementation and demo

Scope: the three commitments on page 5 of the supplied Round 2 submission. The supplied final-round brief requires a working product, repository, final PDF, feature/architecture summary, evidence, roadmap and participant details. It explicitly excludes video and social-media submissions.

## 1. Inspectable evidence

The review engine filters sources by organisation, active version, validity dates and channel, then uses BM25-style lexical ranking with a structured-match boost. The interface displays source text, ID, version, selection reason and score. Whole source records are the passage unit; this is not embeddings or PostgreSQL full-text search. Applicable tone rules and image rules are retained. Different active fact texts sharing an attribute key produce an explicit conflict and incomplete review. The manager resolves a conflict by superseding the outdated source with the agreed fact.

Source snapshots now contain the relevant selected records rather than the entire organisation corpus. Newly added relevant sources also change the snapshot. Old reviews retain conservative organisation-wide invalidation until rerun. Lexical retrieval can miss paraphrases; ranking scores are not confidence estimates. Differently keyed facts can still conflict without detection.

## 2. Controlled corrections

Each finding offers an editable replacement and an exact-change preview. When a quotation occurs repeatedly, the creator selects the occurrence. Saving validates ownership, current revision, completed review, current evidence and exact text offset, then creates an immutable revision and a linked acceptance record. It does not overwrite an existing revision. A stale preview receives HTTP 409. Rejected findings retain reasons and do not bypass high-severity exceptions.

Numeric additions must appear in the cited source or its approved replacement. Naming-rule corrections retain the approved name; numeric corrections preserve configured qualifiers. These are narrow safeguards, not semantic proof of intent. The creator must inspect the resulting draft, and the new revision must pass fresh checks before approval. General edits carry an optimistic revision ID in the browser; legacy API clients omitting that optional field retain the earlier sequential-edit behaviour.

## 3. Revalidation and approval evidence

Affected approved or awaiting-review submissions become `revalidation_required`. Changes to unrelated evidence do not automatically invalidate a new-format approval. Notifications are persisted transactionally with source updates. Expiry is detected on the next inbox, submission-list or detail read. A per-user read marker survives refresh; marking read does not clear revalidation.

This is a durable **in-app inbox**, not email, push delivery or a background scheduler. Reviewers and managers see their organisation's alerts; creators see alerts for their submissions. The approval evidence view and authenticated `/api/submissions/{id}/evidence` export contain the revision, review ID, content hash, source records, findings, reviewer reason and exception reason. Historical decisions remain available after changes.

PostgreSQL tenant advisory locks serialize source changes, reviews, corrections, revision writes and decisions. Four simultaneous-request tests cover duplicate corrections, duplicate reviewer decisions, revision versus approval and source change versus approval. These tests require real PostgreSQL; SQLite skips them. CI provisions PostgreSQL 16 and runs the complete suite against both databases. This is bounded integration coverage, not a load or security certification.

## Evaluation and honest claims

See [FINAL_EVIDENCE.md](FINAL_EVIDENCE.md) for measured outcomes, methodology and limitations. The original 40-case detection fixture is unchanged; baseline and improved live runs are both published. The new prompt policy is grounded in explicit source obligations, naming taxonomy and exact citations. Results reflect combined rules plus hosted semantic review, not standalone model accuracy.

The original 20 correction cases still pass. A separate AI-assisted quality rubric and one explicit creator-edited refinement produce 18 intent-preserving proposals and two unsafe rejections. The refined example is live-verified. This is not independent human assessment; the original worksheet remains available.

## Five-minute demonstration

1. Sign in as Creator. Submit: `India's No. 1 device. Enjoy 20 hours of battery life. Meet NS1.` Use the existing Northstar demo sources.
2. Run checks. Expand ranked evidence and inspect source IDs, versions and quotations. Hosted AI mode requires consent and working provider configuration.
3. Open the battery correction, preview `up to 12 hours`, accept and save. Run checks again. Apply the naming correction. Remove the unsupported ranking phrase using the editable correction, inspecting the resulting punctuation and wording. Save and rerun checks after each change.
4. Request approval. Sign in as Reviewer, inspect the evidence and approve with a reason. Explain that unresolved high findings need an explicit exception.
5. As Manager, add an unrelated warranty fact and confirm approval remains. Supersede the battery fact with a different limit; open the revalidation inbox and show that the original approval evidence remains inspectable.
6. Optional: add a second conflicting active battery fact. Rerun checks and show that the conflict blocks approval. Editing an approved draft also returns it to draft.

## Final-round verification and remaining limits

See [FINAL_EVIDENCE.md](FINAL_EVIDENCE.md) for completed deployment, CI, live journey and live AI evaluation. Baseline and improved 40-case runs are published; limitations remain visible. An AI-assisted correction rubric is complete. Independent human assessment and consented user walkthroughs remain uncompleted. The human worksheet is in HUMAN_ASSESSMENT.md. The final report explicitly declares the unmet assessment rather than substituting automated outputs.

Production onboarding, RLS, migrations, background delivery, rate limiting and broader semantic/visual understanding remain future work. The leader must confirm registration fields and submit before the supplied 30 October 2026 11:59 PM deadline in the organiser's timezone.

AI assistance: implementation, fixtures, tests and documentation were prepared with ChatGPT/Codex assistance. Team members remain responsible for review and explanation. See DISCLOSURES.md for the pre-existing Round 2 baseline and Round 3 changes.

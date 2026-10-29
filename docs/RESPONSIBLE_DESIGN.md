# Privacy, security, accessibility and responsible design

## Privacy and data flow

The public Northstar workspace is a shared fictional demonstration, not a private customer environment. Demo credentials are intentionally visible only when `DEMO_QUICK_FILL=true`. Use synthetic inputs. Drafts, extracted text, source records, comments, decisions and audit records persist in the application database. Original upload bytes are discarded after extraction. There is no self-service retention/deletion policy or reviewed provider-retention agreement; private customer rollout is deferred.

AI processing requires per-revision consent. The server sends draft text, purpose, audience and relevant approved sources to the configured provider. The provider key remains server-side. Provider failures are classified without exposing the raw response or draft in application logs. OCR pixels are not sent to the language model. Hosted database backups and deletion from backups depend on the hosting provider; no instant backup erasure is promised.

## Security controls and limits

Scrypt passwords use random salts; session tokens are hashed in the database, expire and are revoked at logout. API queries are scoped to the authenticated organisation. Role/ownership checks guard source management, corrections, revisions and approvals. Creators cannot approve their own work. SQLAlchemy binds query parameters, and React renders text rather than inserting user HTML.

PostgreSQL advisory/row locks serialize related source and approval changes. Input and upload sizes are bounded; unknown references, stale revisions and invalid citations are rejected. Repository tests cover permission and tenant boundaries. The application audit trail is append-only through its routes, not tamper-proof against a database administrator.

Remaining production work: independent security review, SSO/onboarding, database RLS, formal migrations, rate limiting, per-tenant quotas, retention/deletion controls and stronger operational monitoring. A shared public demo is not an enterprise security boundary. Do not claim a penetration test or security certification.

## Accessibility

Form fields have labels; actions use native buttons; status and errors use text and live regions; severity is written as text as well as colour. Visible keyboard focus styling covers controls and summaries. The layout adapts to narrow screens. Automated browser tests exercise labelled inputs and mobile horizontal fit. These are selected accessibility checks, not full WCAG certification or a screen-reader study.

Alt-text checks are purpose-aware metadata checks. They do not establish that a description is accurate or that an entire campaign is accessible. Image dimensions and standalone-logo hash comparison are deliberately narrow.

## Responsible AI and human control

Source records and uploaded text are untrusted data, not model instructions. The model has no publishing or approval tool. Cited source IDs must belong to the selected evidence, and evidence/issue quotations must match exactly. This proves provenance, not semantic correctness. Missing evidence is not proof a claim is false. Conflicting active facts sharing an attribute key block a complete review.

Corrections are previewed and require a creator action. Numbers, approved names and configured qualifiers receive narrow safeguards; human interpretation of purpose remains necessary. Every saved change needs fresh review. A reviewer records the final decision and any high-severity exception. Unrelated approvals are preserved when their evidence has not changed.

Evaluation fixtures and substantial implementation/documentation assistance are AI-assisted. Team-reported contributions are identified separately. No customer interviews, adoption, revenue, time savings, universal fact checking or independently validated semantic accuracy is invented.

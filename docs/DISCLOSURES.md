# Tools, baseline and assistance disclosure

ChatGPT/Codex assisted with research/proposal drafting, substantial application implementation, evaluation fixtures, tests, debugging and documentation. The team is responsible for reviewing, testing and explaining the submission. AI-generated implementation is significant and is disclosed under General Rule 7.

## Pre-existing baseline versus final-round work

The Round 2 baseline is commit `7a1aceb` (23 October 2026). It already included the deployed React/FastAPI workspace, demo accounts, source checks, hosted AI adapter, revisions and human approvals. It is disclosed as earlier work, not work newly built during Round 3.

Round 3 implementation commits `58eae05`, `abb3347` and `d5e50dc` were recorded on 29 October 2026. They add ranked evidence/conflicts, controlled corrections, dependency-aware revalidation, persistent in-app alerts, PostgreSQL race tests, browser tests and judge documentation. Final verification and evidence publication occurred on 30 October 2026. Git timestamps are evidence of recorded changes, not independent proof of every activity's timing. History has not been rewritten to move earlier work into the window.

The supplied window is 27 October 11:59 PM to 30 October 11:59 PM, 2026. The brief does not specify timezone; the team must use the organiser's timezone. Round 3 changes build on the submitted Round 2 product, as required by the round-specific instructions.

## Reused components

No external application repository or commercial template was reused according to the existing project record. The earlier AI-assisted BrandProof application is the reused baseline. Open-source components include React, TypeScript, Vite, lucide-react, Python, FastAPI, Pydantic, SQLAlchemy, PostgreSQL, pypdf, Pillow, Tesseract, pytest and Playwright. Dependency manifests, lockfile, Dockerfile and workflow identify the versions. Fonts are requested from Google Fonts. Preserve third-party notices and review dependency licences before redistribution.

The live hosted provider is Groq with `openai/gpt-oss-20b` at verification time. No custom model training or external training dataset was used. The Northstar content and evaluation fixtures are fictional and AI-assisted. Fixture labels and retrospective splits are not independent customer validation. No interviews, adoption, revenue, saved hours, penetration test, WCAG certification or independent human intent scores are claimed.

On 30 October, commit 4503217 improves evidence-grounded semantic interpretation, category consistency and bounded malformed-output repair. Baseline and improved evaluations are retained. The correction-quality rubric was assessed by ChatGPT/Codex, with one explicit edited replacement verified live. It is not independent human validation.

# Deploy BrandProof on Render

This Blueprint creates one free Docker web service and one free PostgreSQL database in Singapore. The frontend and API run together. Groq remains the AI provider; the existing Groq key can be used unchanged.

## Setup

1. Sign in at https://dashboard.render.com and connect GitHub.
2. Choose New → Blueprint, select `SinghhSarvesh/brandproof` and branch `main`.
3. Render reads `render.yaml`. Review the two resources and confirm both plans are Free.
4. Enter `AI_API_KEY` privately in the Render prompt. Enter a new random `DEMO_PASSWORD` with at least 16 characters. Do not put either value in chat or GitHub.
5. Apply the Blueprint. Render supplies DATABASE_URL from the private database connection. The Docker startup seeds demo accounts and then starts the app on the platform-assigned port. Repeated seeding does not reset existing passwords.
6. Open the web service's generated onrender.com URL after deployment becomes healthy.

If a free database already exists in the workspace, stop and resolve that limit rather than deleting it or silently upgrading to a paid plan. If Singapore is unavailable for the selected plan, select the same available region for both resources before creating them.

## Accounts and checks

Use `creator@brandproof.demo`, `reviewer@brandproof.demo` or `manager@brandproof.demo` with the private DEMO_PASSWORD. Use fictional materials only. Submit the README sample, enable the AI-processing consent checkbox and run checks. Confirm the semantic review completes with cited evidence; incomplete review is not success. Complete correction, revision, review request and approval using separate accounts.

The configuration is prepared, not proof that deployment or live Groq validation has succeeded. Check deployment logs for startup errors without sharing secrets. If Render shell access is available, `python check_ai.py` makes one live synthetic test request. Otherwise use the review interface.

## Free-tier limits

Render's free web service sleeps after 15 minutes of inactivity, so the first request can be slow. Free PostgreSQL expires after 30 days and is limited to one per workspace. Plan an export or upgrade before expiry if retaining the project. This is a hackathon demo configuration, not a production service guarantee.

Seeding runs at startup because free service support differs from paid pre-deploy hooks. Keep this demo service to one instance. Database migrations, retention/deletion, application rate limiting and wider model evaluation remain tracked in STATUS.md.

References checked 22 October 2026:
- https://render.com/docs/blueprint-spec
- https://render.com/docs/free
- https://render.com/docs/docker

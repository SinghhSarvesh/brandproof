# Deploy BrandProof on Railway with Groq

The repository includes a Railway Docker build, assigned-port support, a pre-deploy seed command and an HTTP health check. This configuration is prepared but is not evidence of a deployed application or a validated live AI service.

## 1. Create the services

Sign in to Railway, choose a workspace and review the plan/credits before creating billable resources. Create a project from `SinghhSarvesh/brandproof`, branch `main`, using the repository root. Add a PostgreSQL database in the same project. The frontend and backend run together in one web container; no separate frontend deployment is required.

## 2. Set backend service variables

In the BrandProof web service, add a reference to the database service's `DATABASE_URL`. Use Railway's variable selector to avoid copying the database password. If the database service is named `Postgres`, the reference is `${{Postgres.DATABASE_URL}}`. Match the actual service name.

| Variable | Value |
| --- | --- |
| DATABASE_URL | Reference to the PostgreSQL service's DATABASE_URL |
| DEMO_PASSWORD | A new random password of at least 16 characters, entered privately |
| REVIEW_MODE | ai |
| AI_PROVIDER_LABEL | Groq |
| AI_BASE_URL | https://api.groq.com/openai/v1 |
| AI_MODEL | openai/gpt-oss-20b |
| AI_API_KEY | Your Groq key, entered privately in Railway variables |

Create a Groq key at https://console.groq.com/keys. Never commit it, include it in screenshots or send it in chat. Confirm model availability for your account and set a spending limit where available. The model must support the `/chat/completions` endpoint and JSON object response mode. Provider/model compatibility must still be tested live.

The initial seed uses DEMO_PASSWORD for three synthetic accounts. Re-seeding does not change their existing passwords. Keep accounts restricted to judges/team members, since a reviewer or manager can make privileged changes. Do not publish the password in README or the repository. Use only synthetic content.

## 3. Deploy

Apply the variables and deploy. `railway.json` selects the Dockerfile, runs `python seed.py` before startup, starts `python start.py` and checks `/api/health`. A seed failure blocks deployment. The process reads Railway's PORT automatically. Never put database initialization or AI keys in the frontend build.

In the web service's Settings → Networking, generate a public domain. Keep the database private; do not expose its TCP port merely to let the application connect. An initial build may fail if database/key variables have not been added yet; configure them and redeploy.

## 4. Verify the deployment

- Open the generated domain and check the login screen.
- Sign in with `creator@brandproof.demo` and the private DEMO_PASSWORD.
- Confirm the interface says AI-assisted review and identifies Groq when requesting processing consent.
- Run `python check_ai.py` in the web service's runtime shell if available. It makes one real model request using fictional text and verifies a cited battery-life contradiction. A passing check is not a model-accuracy evaluation.
- Submit the fictional sample from README, consent to AI processing and run checks. Confirm semantic checks complete; an incomplete result must never be treated as a pass.
- Correct the content, save a new revision and request approval. Sign in as `reviewer@brandproof.demo`, add a reason and approve. Edit again as creator and confirm the new revision needs approval.
- Refresh the page and redeploy once to verify persistence in PostgreSQL.

Manager account: `manager@brandproof.demo`. All three accounts use the private initial DEMO_PASSWORD.

## Troubleshooting

- Database driver error: deployed main includes conversion from postgres/postgresql URLs to the installed psycopg 3 driver. Verify the correct commit was deployed.
- Seed failure: check DATABASE_URL references, private network connectivity and DEMO_PASSWORD length. Existing account passwords are deliberately unchanged by redeploys.
- AI review incomplete: check model availability, API key, provider quota, consent and source validity. Invalid source references or non-JSON output also fail the review.
- OCR failure: the Dockerfile installs Tesseract. Ensure Railway builds with Docker, not a Python-only builder.
- Domain unreachable: inspect deployment health and confirm the service is listening on the platform's PORT.

## References

- https://docs.railway.com/config-as-code/reference
- https://docs.railway.com/deployments/pre-deploy-command
- https://docs.railway.com/variables
- https://console.groq.com/docs/openai
- https://console.groq.com/docs/model/openai/gpt-oss-20b

Provider documentation checked 22 October 2026. Hosting/model usage may incur charges; account billing and quotas remain under the owner's control.

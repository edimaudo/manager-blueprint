# Manager Blueprint — FastAPI + Supabase + Gemini

A server-rendered FastAPI application for management development. The supplied landing page was preserved as the starting point and its previous access-choice section was replaced with three plan feature cards. No plan prices were invented because none were supplied.

## Plans

- **Free:** limited management coaching, management articles, limited tools/templates.
- **Manager Plus:** more coaching access, articles and downloads, management-style reflection, coaching diary and development updates, new management thinking/approaches, tools/templates.
- **Manager Pro:** increased coaching access, management articles and downloads, management-style reflection, coaching diary and updates, new management-thinking articles, tools/templates.

Actual amounts and payment processor are intentionally not configured yet. Paid entitlement must be assigned server-side after a verified billing event; signup never grants a paid tier.

## Stack

- FastAPI + Jinja2
- Supabase Auth and Postgres with Row Level Security
- Private Supabase Storage for administrator-published PDFs/text documents
- Google GenAI SDK (`google-genai`) with `gemini-3.6-flash`
- Docker container intended for Google Cloud Run

## Local setup

1. Create a Supabase project.
2. Apply `supabase/migrations/202610250001_initial_schema.sql` using the Supabase CLI or SQL editor.
3. Ensure the private Storage bucket `management-library` is created by the migration.
4. Copy `.env.example` to `.env`, fill in the Supabase URL, publishable/anon key, server-only service role key, Google API key, and generate a Fernet encryption key:

   ```bash
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
   ```

5. Install and run:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn app:app --reload
   ```

6. Create a user at `/signup`. The Supabase project must have email/password authentication enabled. If email confirmation is enabled, confirm the email before sign-in.
7. Administrator login is at `/admin/login`. The user must have `app_metadata.role=admin`; ordinary users cannot set this metadata.

## Demo accounts

Demo accounts cannot be created from this repository without access to your Supabase project. To create four actual Supabase Auth accounts in your own project, set `DEMO_ACCOUNTS_ENABLED=true` and run:

```bash
python scripts/seed_demo_users.py
```

The script creates/resets `demo-free@managerblueprint.local`, `demo-plus@managerblueprint.local`, `demo-pro@managerblueprint.local`, and `demo-admin@managerblueprint.local`. It generates strong random passwords and writes them to `.demo-credentials.txt` with restrictive permissions where supported. Do not commit this file. Rotate/delete demo accounts before production. `Manager Plus`/`Manager Pro` demo accounts are for entitlement testing, not payment accounts.

## Admin knowledge library

The administrator page supports PDF, TXT, and Markdown uploads. Documents are stored in a private Supabase Storage bucket. Extracted text is chunked into `document_chunks` for contextual coaching. A document's access tier controls whether a user can retrieve its metadata/content. PDF viewing is available for published free documents; document downloads require Plus or Pro. For PDF viewing to work reliably in browser, the backend streams the original bytes with `Content-Disposition: inline`.

The coaching system uses uploaded and published text as reference context. It does not crawl and republish TickTick, Asana, monday.com, or Strawberry.me content. Article links point to the publishers' original pages. Only upload material you have permission to use. The management-style reflection is an original developmental tool informed by public descriptions of DISC-style behavior; it does not reproduce official CliftonStrengths or Everything DiSC question banks or claim to be a validated psychometric instrument.

## Security design

- Supabase Auth handles password verification and user identity.
- The browser receives only an encrypted, HttpOnly, SameSite=Lax session cookie. The cookie is Secure in production. Access and refresh tokens are encrypted with `APP_ENCRYPTION_KEY` before cookie storage.
- `SUPABASE_SERVICE_ROLE_KEY` is backend-only. Never put it in HTML, JavaScript, or a `NEXT_PUBLIC_*` variable.
- Database tables have RLS enabled and explicit grants/policies. Personal data is filtered by `auth.uid()`. Admin privileges require server-assigned `app_metadata.role=admin`.
- Storage bucket is private; downloads are proxied through server authorization.
- Responses use baseline security headers; production enables HSTS.
- Set `APP_ENV=production`, HTTPS, a strong secret, and Cloud Run Secret Manager mappings in production.
- Configure Supabase Auth rate limits, email confirmation, password policy, MFA for admins, Cloud Armor / edge rate limits, alerting, backups, and log retention before public launch.
- The admin activity screen is sensitive. Restrict admin access, avoid logging user prompts or full diary entries, and define a retention policy.

## Important production gaps

This is a functional integration scaffold, not a claim of production certification. Billing webhooks and subscription checkout are not implemented because a provider and prices have not been specified. User sign-up always starts at Free. Add a verified billing webhook that updates trusted `app_metadata.tier` or a server-managed entitlement table. The current article sources are publisher links; automatic feed ingestion should use official RSS/API or permissioned feeds, with source URL and publication date retained. Implement robust request rate limiting, CSRF tokens for clients that omit Origin/Referer (same-origin checks are present as a baseline), email verification flows, audit-log retention, antivirus scanning for uploads, and RLS integration tests with distinct user JWTs before production.

## Run tests

```bash
pytest -q
```

The local tests cover route and model contracts without requiring live credentials. Database policy tests should run with Supabase CLI after configuring the local Supabase stack.

## Cloud Run

Build and deploy the container with a Cloud Run service account and secrets from Secret Manager. Do not bake `.env` into the image. Set `APP_BASE_URL` to the deployed HTTPS service URL. Configure `PORT` (Cloud Run supplies this), map secrets from Secret Manager, set minimum/maximum instances, concurrency, timeouts, and service-level IAM/networking according to the expected traffic and privacy requirements.

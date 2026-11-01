# Manager Blueprint — FastAPI + Supabase + Gemini

A server-rendered FastAPI application for management development. Vercel remains the current hosting target. The Dockerfile and Cloud Run notes are retained only as an optional future migration path; they are not required for the current deployment.

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
- FastAPI ASGI application for the current Vercel deployment
- The root `app.py` exports `app` as the FastAPI entry point; `.python-version` pins Python 3.12, and `static/` is mounted through FastAPI `StaticFiles`. Continue using the existing Vercel project and its current domain. Vercel documents this FastAPI entry-point pattern and static-file support in its [FastAPI deployment guide](https://vercel.com/docs/frameworks/backend/fastapi).
- Dockerfile retained for a future, optional Google Cloud Run migration

## Local setup

1. Create a Supabase project.
2. Apply `supabase/migrations/202610250001_initial_schema.sql` using the Supabase CLI or SQL editor.
3. Apply `supabase/migrations/202611010001_manager_development_features.sql` after the initial migration. It adds capability progress and saved coaching sessions/messages, and adds the capability slug to selected goals.
4. Ensure the private Storage bucket `management-library` is created by the initial migration.
5. Copy `.env.example` to `.env`, fill in the Supabase URL, publishable/anon key, server-only service role key, Google API key, and generate a Fernet encryption key:

   ```bash
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
   ```

6. Install and run:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn app:app --reload
   ```

7. Create a user at `/signup`. The Supabase project must have email/password authentication enabled. If email confirmation is enabled, confirm the email before sign-in.
8. Administrator login is at `/admin/login`. The user must have `app_metadata.role=admin`; ordinary users cannot set this metadata.

## Demo accounts

Demo accounts cannot be created from this repository without access to your Supabase project. To create four actual Supabase Auth accounts in your own project, set `DEMO_ACCOUNTS_ENABLED=true` and run:

```bash
python scripts/seed_demo_users.py
```

The script creates/resets `demo-free@managerblueprint.local`, `demo-plus@managerblueprint.local`, `demo-pro@managerblueprint.local`, and `demo-admin@managerblueprint.local`. It generates strong random passwords and writes them to `.demo-credentials.txt` with restrictive permissions where supported. Do not commit this file. Rotate/delete demo accounts before production. `Manager Plus`/`Manager Pro` demo accounts are for entitlement testing, not payment accounts.

## Manager Blueprint capability experience

The Blueprint now organizes 18 management capabilities across Managing Yourself, Managing Others, and Managing Up. Each capability provides Learn, Apply, Practice, and Assess stages, with one mapped role-play scenario per capability. Capability progress is stored in `capability_progress`; completed worksheets, role-play practice, and self-reflections contribute to the progress view and coaching context. The onboarding baseline has been expanded to 18 capability questions and records domain and capability-level scores.

The management-style reflection retains its 12 original questions, but results now show close behavioral and strengths-domain patterns rather than forcing a single dominant category. Results include a combined archetype, score distributions, potential strengths and watch-outs, a suggested management approach, and a comparison with the previous reflection. It remains an original development reflection, not a validated psychometric test.

AI coaching now receives management stage, selected goals, latest capability baseline, management-style reflection, coach preference, recent diary entries, and capability progress. Coaching conversations are saved in private `coaching_sessions` and `coaching_messages` tables and can be resumed. Role-play scenarios are mapped to capabilities; requesting a debrief completes the Practice step.

The initial resource catalogue is curated from monday.com, Asana, and TickTick pages. It uses original short summaries and links to publisher pages. Relevant short summaries are passed to the coach as signposts; full external article text is not scraped or ingested. Canadian Tire, Manulife, and Home Depot documentation has not yet been supplied and is intentionally not included; see `SOURCES.md` for the future content intake approach.

## Admin knowledge library

The administrator page supports PDF, TXT, and Markdown uploads. Documents are stored in a private Supabase Storage bucket. Extracted text is chunked into `document_chunks` for contextual coaching. A document's access tier controls whether a user can retrieve its metadata/content. PDF viewing is available for published free documents; document downloads require Plus or Pro. For PDF viewing to work reliably in browser, the backend streams the original bytes with `Content-Disposition: inline`.

The coaching system uses approved uploaded document excerpts as grounded reference context and short curated publisher summaries as resource signposts. It does not crawl, ingest, or republish full external articles. Article links point to the publishers' original pages. Only upload material you have permission to use. The management-style reflection is an original developmental tool informed by public descriptions of DISC-style behavior; it does not reproduce official CliftonStrengths or Everything DiSC question banks or claim to be a validated psychometric instrument.

## Security design

- Supabase Auth handles password verification and user identity.
- The browser receives only an encrypted, HttpOnly, SameSite=Lax session cookie. The cookie is Secure in production. Access and refresh tokens are encrypted with `APP_ENCRYPTION_KEY` before cookie storage.
- `SUPABASE_SERVICE_ROLE_KEY` is backend-only. Never put it in HTML, JavaScript, or a `NEXT_PUBLIC_*` variable.
- Database tables have RLS enabled and explicit grants/policies. Personal data is filtered by `auth.uid()`. Admin privileges require server-assigned `app_metadata.role=admin`.
- Storage bucket is private; downloads are proxied through server authorization.
- Responses use baseline security headers; production enables HSTS.
- Set `APP_ENV=production`, HTTPS, and strong secrets in Vercel Environment Variables for the current deployment. If Cloud Run is adopted later, map those secrets through Google Cloud Secret Manager.
- Configure Supabase Auth rate limits, email confirmation, password policy, MFA for admins, Cloud Armor / edge rate limits, alerting, backups, and log retention before public launch.
- The admin activity screen is sensitive. Restrict admin access, avoid logging user prompts or full diary entries, and define a retention policy.

## Important production gaps

This is a functional integration scaffold, not a claim of production certification. Billing webhooks and subscription checkout are not implemented because a provider and prices have not been specified. User sign-up always starts at Free. Add a verified billing webhook that updates trusted `app_metadata.tier` or a server-managed entitlement table. The current Free coaching safeguard defaults to five messages per day through `FREE_COACH_DAILY_LIMIT`; this is configurable and is an interim protection, not a finalized commercial allowance. The current article sources are publisher links; automatic feed ingestion should use official RSS/API or permissioned feeds, with source URL and publication date retained. Implement robust request rate limiting, CSRF tokens for clients that omit Origin/Referer (same-origin checks are present as a baseline), email verification flows, audit-log retention, antivirus scanning for uploads, and RLS integration tests with distinct user JWTs before production.

## Run tests

```bash
pytest -q
```

The local tests cover route and model contracts without requiring live credentials. Database policy tests should run with Supabase CLI after configuring the local Supabase stack.

## Optional future Cloud Run migration

Cloud Run is not part of the current release path. Keep the Dockerfile and this section available for a future migration when a new domain and hosting decision are made. Until then, continue using the existing Vercel deployment and its current routing/configuration. Do not change hosting solely to complete the feature work in this release.

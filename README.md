# Manager Blueprint

This repository contains the Manager Blueprint application source. The uploaded requirements in `PRD.md` are the product source of truth. Implementation decisions and remaining gaps are recorded in `BUILD_STATUS.md`.

## Product structure

Manager Blueprint is one manager-development application centered on the user's personalized Blueprint. Management capabilities are organized under Managing Yourself, Managing Others, and Managing Up. Tools, templates, practice, assessments, and AI coaching are contextual capabilities within the Blueprint, not separate products or primary navigation destinations.

The product supports independent access paths:

- Free access
- One-time purchases of individual management resources
- Manager Plus subscription
- Manager Pro subscription

A user can combine one-time purchases with a subscription.

## Current build

The v13 increment adds production configuration checks, origin/host validation, security headers, request/document bounds, and an asynchronous Gemini timeout. The v12 increment adds monthly entitlement enforcement and opt-in aggregate style-assessment pilot analysis. The v11 increment replaces the 12-item reflection with an algorithm-scored 32-statement Manager Style Profile and converts billing to provider-neutral, disabled placeholders. The v10 increment applies the PRD sky-blue accent to a neutral charcoal dark theme throughout the application. The v7 increment simplified the public landing page, removed eyebrow/kicker labels across application templates, and applied the PRD brand palette in the shared and landing-page stylesheets. The landing page contains a product-specific headline, short explanation, Blueprint preview, two concise value explanations, and a clear signup action. The app retains Inter, light/dark mode, and text/interface scaling at 0.75x, 1x, and 1.25x.

See `BUILD_STATUS.md` for verification results and remaining product requirements.

## Existing implementation technology

The inherited source currently contains:

- FastAPI and Jinja2
- Supabase Auth, Postgres/RLS, and private object storage
- Provider-neutral billing catalogue and entitlement foundation; checkout is disabled pending payment-provider selection
- Google Gemini coaching integration

These integrations were present in the existing source archive. The uploaded product PRD does not prescribe a technology stack, database, authentication provider, hosting provider, or AI model provider. They are retained for continuity only and are not a final approved architecture decision. Confirm the infrastructure choices before production deployment or additional infrastructure work.

## Local setup for the inherited source

The current source requires the environment variables documented in `.env.example`. It will not run as a fully functional application until its existing external services are configured.

1. Create a Python virtual environment.
2. Install the dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Configure the existing environment variables in `.env`. The current backend expects Supabase credentials, an encryption key, and a Gemini API key. Billing is intentionally a placeholder; no payment credentials are required or accepted.
4. If continuing with the inherited Supabase backend, apply these migrations in this order:
   - `supabase/migrations/202610250001_initial_schema.sql`
   - `supabase/migrations/202611010001_manager_development_features.sql`
   - `supabase/migrations/202611020001_progress_and_practice.sql`
   - `supabase/migrations/202611060001_billing_foundation.sql`
   - `supabase/migrations/202611110001_billing_provider_neutral.sql`
   - `supabase/migrations/202611120001_monthly_quotas_and_style_pilot.sql`
5. Run the app:

   ```bash
   uvicorn app:app --reload
   ```

6. Open `http://localhost:8000`.

Do not deploy this inherited stack as an approved production architecture solely because it is present in the repository.

## Tests

Run the automated tests with:

```bash
pytest -q
```

The tests exercise local application logic and route/template contracts. They do not validate live Supabase, Gemini credentials, browser accessibility, external security, deployment, or backup recovery. Billing checkout is intentionally disabled.

## Article and assessment constraints

External publisher resources use original summaries and links to the publisher. The app does not scrape, mirror, or republish full external articles.

The Manager Style Profile contains 32 original management-behaviour statements across four behavioural-preference dimensions and four contribution domains. It is informed by publicly described concepts associated with DiSC and CliftonStrengths, but it is not an official assessment and does not reproduce proprietary question banks or claim validated psychometric status. Licensed proprietary materials should only be introduced with the required permissions.

## Phase 1 and Phase 4 migration

Before deploying the v12 increment, apply:

```bash
supabase db push
```

This applies `supabase/migrations/202611120001_monthly_quotas_and_style_pilot.sql` in the linked Supabase project. Confirm the migration is applied before deploying the application code. The app uses the server-side `SUPABASE_SERVICE_ROLE_KEY` for atomic quota consumption and admin-only aggregate pilot analysis; never expose it in frontend variables.

Monthly quotas use UTC calendar months and unique item identifiers: Free = one unique tool/template and five unique articles/resources; Manager Plus = three unique tools/templates; Manager Pro = uncapped. Reopening the same item in the same month does not consume another quota slot. Billing remains disabled and provider-neutral.

The optional pilot consent checkbox is not required to complete the Manager Style Profile. Only opt-in submissions are included in `/admin/style-validation` and `/api/admin/style-validation`.

## Priority 5 — Production readiness

See `PRODUCTION_ACCEPTANCE.md` for the release checklist and `SECURITY_PRIVACY_REVIEW.md` for implemented controls and outstanding risks. Production startup requires `APP_ENV=production`, exact HTTPS origins/hosts, Supabase server secrets, a valid `APP_ENCRYPTION_KEY`, and `GOOGLE_API_KEY` for coaching. Set `APP_ALLOWED_ORIGINS` and `APP_ALLOWED_HOSTS` in the deployment environment; see `.env.example`.

`/health` is a liveness endpoint. `/ready` validates required configuration only; neither endpoint proves that Supabase or Gemini is reachable. The current build is not production-approved until live integration, RLS, accessibility, staging, monitoring, and recovery checks are completed.

## Supplied content folder

The `content/` directory is the source-material staging area for management content supplied for Manager Blueprint. It includes separate folders for knowledge, frameworks, tools/templates, practice scenarios, coaching guidance, and assessment references. See `content/README.md` for the folder guide, supported formats, review requirements, and the process for publishing content. Files placed in this folder are not automatically imported into the live application. Approved PDF, TXT, and Markdown documents are currently uploaded and indexed through the admin page.

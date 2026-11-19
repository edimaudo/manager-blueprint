-- Convert any previously-created Stripe-shaped billing records into a
-- provider-neutral schema. Safe to apply after the original or revised billing
-- foundation migration.

create table if not exists public.billing_provider_customers (
  user_id uuid not null references auth.users(id) on delete cascade,
  provider_key text not null,
  provider_customer_ref text not null,
  created_at timestamptz not null default now(),
  primary key (user_id, provider_key),
  unique (provider_key, provider_customer_ref)
);

alter table public.billing_purchases add column if not exists provider_key text;
alter table public.billing_purchases add column if not exists provider_transaction_ref text;
alter table public.billing_subscriptions add column if not exists provider_key text;
alter table public.billing_subscriptions add column if not exists provider_subscription_ref text;

DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema='public' AND table_name='billing_purchases' AND column_name='stripe_checkout_session_id') THEN
    EXECUTE 'UPDATE public.billing_purchases SET provider_key = COALESCE(provider_key, ''stripe''), provider_transaction_ref = COALESCE(provider_transaction_ref, stripe_checkout_session_id) WHERE stripe_checkout_session_id IS NOT NULL';
    EXECUTE 'ALTER TABLE public.billing_purchases DROP COLUMN stripe_checkout_session_id';
  END IF;
  IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema='public' AND table_name='billing_purchases' AND column_name='stripe_payment_intent_id') THEN
    EXECUTE 'ALTER TABLE public.billing_purchases DROP COLUMN stripe_payment_intent_id';
  END IF;
  IF EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema='public' AND table_name='billing_subscriptions' AND column_name='stripe_subscription_id') THEN
    EXECUTE 'UPDATE public.billing_subscriptions SET provider_key = COALESCE(provider_key, ''stripe''), provider_subscription_ref = COALESCE(provider_subscription_ref, stripe_subscription_id) WHERE stripe_subscription_id IS NOT NULL';
    EXECUTE 'ALTER TABLE public.billing_subscriptions DROP COLUMN stripe_subscription_id';
  END IF;
END $$;

create unique index if not exists billing_purchases_provider_ref_idx
  on public.billing_purchases(provider_key, provider_transaction_ref)
  where provider_transaction_ref is not null;
create unique index if not exists billing_subscriptions_provider_ref_idx
  on public.billing_subscriptions(provider_key, provider_subscription_ref)
  where provider_subscription_ref is not null;

DO $$
BEGIN
  IF to_regclass('public.stripe_customers') IS NOT NULL THEN
    EXECUTE 'INSERT INTO public.billing_provider_customers(user_id, provider_key, provider_customer_ref) SELECT user_id, ''stripe'', stripe_customer_id FROM public.stripe_customers ON CONFLICT DO NOTHING';
    EXECUTE 'DROP TABLE public.stripe_customers CASCADE';
  END IF;
END $$;

create table if not exists public.billing_webhook_events (
  provider_key text not null,
  event_id text not null,
  event_type text not null,
  received_at timestamptz not null default now(),
  primary key (provider_key, event_id)
);

DO $$
BEGIN
  IF to_regclass('public.stripe_webhook_events') IS NOT NULL THEN
    EXECUTE 'INSERT INTO public.billing_webhook_events(provider_key, event_id, event_type, received_at) SELECT ''stripe'', event_id, event_type, received_at FROM public.stripe_webhook_events ON CONFLICT DO NOTHING';
    EXECUTE 'DROP TABLE public.stripe_webhook_events CASCADE';
  END IF;
END $$;

alter table public.billing_provider_customers enable row level security;
alter table public.billing_webhook_events enable row level security;
drop policy if exists billing_provider_customers_select_own on public.billing_provider_customers;
create policy billing_provider_customers_select_own on public.billing_provider_customers for select to authenticated using (auth.uid() = user_id);
revoke all on public.billing_provider_customers, public.billing_webhook_events from anon;
grant select on public.billing_provider_customers to authenticated;
grant all on public.billing_provider_customers, public.billing_webhook_events to service_role;

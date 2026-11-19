-- Provider-neutral billing foundation for Manager Blueprint.
-- No payment processor is connected by this migration.
create table if not exists public.billing_provider_customers (
  user_id uuid not null references auth.users(id) on delete cascade,
  provider_key text not null,
  provider_customer_ref text not null,
  created_at timestamptz not null default now(),
  primary key (user_id, provider_key),
  unique (provider_key, provider_customer_ref)
);

create table if not exists public.billing_purchases (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  product_key text not null,
  provider_key text,
  provider_transaction_ref text,
  status text not null check (status in ('paid','refunded','disputed','pending')),
  purchased_at timestamptz not null default now(),
  created_at timestamptz not null default now(),
  unique (provider_key, provider_transaction_ref)
);

create table if not exists public.billing_subscriptions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  product_key text not null,
  provider_key text,
  provider_subscription_ref text,
  status text not null,
  current_period_end timestamptz,
  cancel_at_period_end boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (provider_key, provider_subscription_ref)
);

create table if not exists public.billing_entitlements (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  entitlement_key text not null,
  source_type text not null check (source_type in ('purchase','subscription','admin_grant')),
  source_id text not null,
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  unique(user_id, entitlement_key, source_type, source_id)
);

create table if not exists public.billing_webhook_events (
  provider_key text not null,
  event_id text not null,
  event_type text not null,
  received_at timestamptz not null default now(),
  primary key (provider_key, event_id)
);

create index if not exists billing_purchases_user_idx on public.billing_purchases(user_id, purchased_at desc);
create index if not exists billing_subscriptions_user_idx on public.billing_subscriptions(user_id, status);
create index if not exists billing_entitlements_user_active_idx on public.billing_entitlements(user_id, is_active, entitlement_key);

alter table public.billing_provider_customers enable row level security;
alter table public.billing_purchases enable row level security;
alter table public.billing_subscriptions enable row level security;
alter table public.billing_entitlements enable row level security;
alter table public.billing_webhook_events enable row level security;

drop policy if exists billing_provider_customers_select_own on public.billing_provider_customers;
create policy billing_provider_customers_select_own on public.billing_provider_customers for select to authenticated using (auth.uid() = user_id);
drop policy if exists billing_purchases_select_own on public.billing_purchases;
create policy billing_purchases_select_own on public.billing_purchases for select to authenticated using (auth.uid() = user_id);
drop policy if exists billing_subscriptions_select_own on public.billing_subscriptions;
create policy billing_subscriptions_select_own on public.billing_subscriptions for select to authenticated using (auth.uid() = user_id);
drop policy if exists billing_entitlements_select_own on public.billing_entitlements;
create policy billing_entitlements_select_own on public.billing_entitlements for select to authenticated using (auth.uid() = user_id);

revoke all on public.billing_provider_customers, public.billing_purchases, public.billing_subscriptions, public.billing_entitlements, public.billing_webhook_events from anon;
grant select on public.billing_provider_customers, public.billing_purchases, public.billing_subscriptions, public.billing_entitlements to authenticated;
grant all on public.billing_provider_customers, public.billing_purchases, public.billing_subscriptions, public.billing_entitlements, public.billing_webhook_events to service_role;

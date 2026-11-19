-- Phase 1: server-enforced monthly allowances. Usage is counted in UTC calendar months.
create table if not exists public.monthly_usage_items (
  user_id uuid not null references auth.users(id) on delete cascade,
  quota_key text not null check (quota_key in ('tool','article')),
  period_start date not null,
  item_key text not null,
  created_at timestamptz not null default now(),
  primary key (user_id, quota_key, period_start, item_key)
);

create table if not exists public.monthly_usage (
  user_id uuid not null references auth.users(id) on delete cascade,
  quota_key text not null check (quota_key in ('tool','article')),
  period_start date not null,
  usage_count integer not null default 0 check (usage_count >= 0),
  updated_at timestamptz not null default now(),
  primary key (user_id, quota_key, period_start)
);

alter table public.monthly_usage enable row level security;
alter table public.monthly_usage_items enable row level security;
revoke all on public.monthly_usage, public.monthly_usage_items from anon, authenticated;
grant all on public.monthly_usage, public.monthly_usage_items to service_role;

create or replace function public.consume_monthly_quota(
  p_user_id uuid,
  p_quota_key text,
  p_limit integer,
  p_item_key text
) returns jsonb
language plpgsql
security definer
set search_path = public, pg_temp
as $$
declare
  v_period_start date := date_trunc('month', timezone('utc', now()))::date;
  v_used integer;
  v_allowed boolean := false;
  v_new_item boolean := false;
begin
  if p_quota_key not in ('tool','article') then
    raise exception 'Unsupported quota key';
  end if;
  if p_limit < 1 then raise exception 'Quota limit must be positive'; end if;
  if p_item_key is null or length(trim(p_item_key)) = 0 then raise exception 'Quota item key is required'; end if;

  insert into public.monthly_usage_items(user_id, quota_key, period_start, item_key)
  values (p_user_id, p_quota_key, v_period_start, p_item_key)
  on conflict do nothing
  returning true into v_new_item;

  if not coalesce(v_new_item, false) then
    select usage_count into v_used from public.monthly_usage
    where user_id = p_user_id and quota_key = p_quota_key and period_start = v_period_start;
    return jsonb_build_object('allowed', true, 'already_counted', true, 'used', coalesce(v_used,0),
      'limit', p_limit, 'remaining', greatest(0,p_limit-coalesce(v_used,0)), 'period_start', v_period_start);
  end if;

  insert into public.monthly_usage(user_id, quota_key, period_start, usage_count, updated_at)
  values (p_user_id, p_quota_key, v_period_start, 1, now())
  on conflict (user_id, quota_key, period_start)
  do update set usage_count = public.monthly_usage.usage_count + 1, updated_at = now()
  where public.monthly_usage.usage_count < p_limit
  returning usage_count into v_used;

  if found then
    v_allowed := true;
  else
    delete from public.monthly_usage_items
    where user_id = p_user_id and quota_key = p_quota_key and period_start = v_period_start and item_key = p_item_key;
    select usage_count into v_used
    from public.monthly_usage
    where user_id = p_user_id and quota_key = p_quota_key and period_start = v_period_start;
    v_used := coalesce(v_used, 0);
  end if;

  return jsonb_build_object(
    'allowed', v_allowed,
    'already_counted', false,
    'used', v_used,
    'limit', p_limit,
    'remaining', greatest(0, p_limit - v_used),
    'period_start', v_period_start
  );
end;
$$;

revoke all on function public.consume_monthly_quota(uuid,text,integer,text) from public, anon, authenticated;
grant execute on function public.consume_monthly_quota(uuid,text,integer,text) to service_role;

-- Phase 4: explicit opt-in for de-identified, aggregate assessment pilot analysis.
alter table public.style_assessments
  add column if not exists pilot_consent boolean not null default false;
create index if not exists style_assessments_pilot_consent_created
  on public.style_assessments(created_at)
  where pilot_consent = true;

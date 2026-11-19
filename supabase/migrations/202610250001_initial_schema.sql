-- Manager Blueprint Supabase schema. Apply via Supabase CLI migrations.
create extension if not exists pgcrypto;

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text,
  management_stage text check (management_stage in ('aspiring','first_time','experienced','senior','director')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create table if not exists public.user_goals (
  id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id) on delete cascade,
  domain text not null check (domain in ('yourself','others','up')), capability text not null, priority smallint not null default 3 check(priority between 1 and 5),
  created_at timestamptz not null default now()
);
create table if not exists public.baseline_assessments (
  id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id) on delete cascade,
  answers jsonb not null, result jsonb not null, created_at timestamptz not null default now()
);
create index if not exists baseline_assessments_user_created on public.baseline_assessments(user_id, created_at desc);
create table if not exists public.style_assessments (
  id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id) on delete cascade,
  answers jsonb not null, result jsonb not null, created_at timestamptz not null default now()
);
create index if not exists style_assessments_user_created on public.style_assessments(user_id, created_at desc);
create table if not exists public.coach_preferences (
  id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id) on delete cascade,
  answers jsonb not null, result jsonb not null, created_at timestamptz not null default now()
);
create table if not exists public.coaching_diary (
  id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id) on delete cascade,
  entry text not null check (char_length(entry) <= 12000), next_step text not null default '', created_at timestamptz not null default now()
);
create index if not exists coaching_diary_user_created on public.coaching_diary(user_id, created_at desc);
create table if not exists public.documents (
  id uuid primary key default gen_random_uuid(), title text not null, summary text not null default '', filename text not null,
  storage_path text unique, access_tier text not null default 'free' check(access_tier in ('free','plus','pro')),
  document_type text not null check(document_type in ('pdf','article','text')), is_published boolean not null default false,
  source_url text, uploaded_by uuid references auth.users(id) on delete set null, published_at timestamptz,
  created_at timestamptz not null default now()
);
create table if not exists public.document_chunks (
  id uuid primary key default gen_random_uuid(), document_id uuid not null references public.documents(id) on delete cascade,
  title text not null, content text not null, chunk_index integer not null, access_tier text not null check(access_tier in ('free','plus','pro')),
  is_published boolean not null default false, source_url text, created_at timestamptz not null default now(),
  content_tsv tsvector generated always as (to_tsvector('english'::regconfig, coalesce(title,'') || ' ' || coalesce(content,''))) stored,
  unique(document_id, chunk_index)
);
create index if not exists document_chunks_published_tier on public.document_chunks(is_published, access_tier);
create index if not exists document_chunks_content_tsv on public.document_chunks using gin(content_tsv);
create table if not exists public.app_events (
  id uuid primary key default gen_random_uuid(), user_id uuid references auth.users(id) on delete set null,
  event_type text not null, metadata jsonb not null default '{}'::jsonb, created_at timestamptz not null default now()
);
create index if not exists app_events_created on public.app_events(created_at desc);
create table if not exists public.usage_counters (
  id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id) on delete cascade,
  usage_type text not null, usage_date date not null default current_date, count integer not null default 0 check(count >= 0),
  unique(user_id, usage_type, usage_date)
);

-- New users receive a profile. Paid entitlement is deliberately not derived from user-editable user_metadata.
create or replace function public.handle_new_user() returns trigger language plpgsql security definer set search_path = '' as $$
begin
  insert into public.profiles(id, display_name) values (new.id, coalesce(new.raw_user_meta_data->>'display_name','')) on conflict(id) do nothing;
  return new;
end; $$;
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users for each row execute procedure public.handle_new_user();

-- Enable RLS everywhere exposed. Admin/service key must never be sent to the browser.
alter table public.profiles enable row level security;
alter table public.user_goals enable row level security;
alter table public.baseline_assessments enable row level security;
alter table public.style_assessments enable row level security;
alter table public.coach_preferences enable row level security;
alter table public.coaching_diary enable row level security;
alter table public.documents enable row level security;
alter table public.document_chunks enable row level security;
alter table public.app_events enable row level security;
alter table public.usage_counters enable row level security;

revoke all on public.profiles,public.user_goals,public.baseline_assessments,public.style_assessments,public.coach_preferences,public.coaching_diary,public.documents,public.document_chunks,public.app_events,public.usage_counters from anon;
revoke all on public.profiles,public.user_goals,public.baseline_assessments,public.style_assessments,public.coach_preferences,public.coaching_diary,public.documents,public.document_chunks,public.app_events,public.usage_counters from authenticated;
grant select,update on public.profiles to authenticated;
grant select,insert,update,delete on public.user_goals,public.baseline_assessments,public.style_assessments,public.coach_preferences,public.coaching_diary to authenticated;
grant select on public.documents,public.document_chunks to authenticated;
grant select,insert on public.app_events to authenticated;
grant select on public.usage_counters to authenticated;

create policy profiles_select_own on public.profiles for select to authenticated using ((select auth.uid())=id or (auth.jwt()->'app_metadata'->>'role')='admin');
create policy profiles_update_own_nonprivileged on public.profiles for update to authenticated using ((select auth.uid())=id) with check ((select auth.uid())=id);
create policy goals_own_all on public.user_goals for all to authenticated using ((select auth.uid())=user_id) with check ((select auth.uid())=user_id);
create policy baseline_own_all on public.baseline_assessments for all to authenticated using ((select auth.uid())=user_id) with check ((select auth.uid())=user_id);
create policy style_own_all on public.style_assessments for all to authenticated using ((select auth.uid())=user_id) with check ((select auth.uid())=user_id);
create policy coach_preferences_own_all on public.coach_preferences for all to authenticated using ((select auth.uid())=user_id) with check ((select auth.uid())=user_id);
create policy diary_own_all on public.coaching_diary for all to authenticated using ((select auth.uid())=user_id) with check ((select auth.uid())=user_id);
create policy events_insert_own on public.app_events for insert to authenticated with check ((select auth.uid())=user_id);
create policy events_select_own_or_admin on public.app_events for select to authenticated using ((select auth.uid())=user_id or (auth.jwt()->'app_metadata'->>'role')='admin');
create policy usage_select_own on public.usage_counters for select to authenticated using ((select auth.uid())=user_id);
create policy docs_select_by_entitlement on public.documents for select to authenticated using (is_published and ((access_tier='free') or (access_tier='plus' and auth.jwt()->'app_metadata'->>'tier' in ('plus','pro')) or (access_tier='pro' and auth.jwt()->'app_metadata'->>'tier'='pro') or auth.jwt()->'app_metadata'->>'role'='admin'));
create policy chunks_select_by_entitlement on public.document_chunks for select to authenticated using (is_published and ((access_tier='free') or (access_tier='plus' and auth.jwt()->'app_metadata'->>'tier' in ('plus','pro')) or (access_tier='pro' and auth.jwt()->'app_metadata'->>'tier'='pro') or auth.jwt()->'app_metadata'->>'role'='admin'));

-- Private Storage bucket. Storage policies deny direct browser access; the backend proxies authorized downloads.
insert into storage.buckets(id,name,public,file_size_limit,allowed_mime_types) values ('management-library','management-library',false,20971520,array['application/pdf','text/plain','text/markdown']) on conflict(id) do update set public=false,file_size_limit=20971520;
drop policy if exists "No direct client reads for management library" on storage.objects;
-- No client-facing policy is created for this bucket, so direct client reads are denied.
-- Admin uploads and authorized document streaming are performed server-side with the service role.

create policy docs_admin_all on public.documents for select to authenticated using ((auth.jwt()->'app_metadata'->>'role')='admin');
create policy chunks_admin_all on public.document_chunks for select to authenticated using ((auth.jwt()->'app_metadata'->>'role')='admin');

-- Atomic free-coaching quota: only the server's service role may call this function.
create or replace function public.consume_coach_quota(p_user_id uuid, p_limit integer default 5)
returns integer language plpgsql security definer set search_path = '' as $$
declare new_count integer;
begin
  insert into public.usage_counters(user_id,usage_type,usage_date,count)
  values (p_user_id,'coach',current_date,1)
  on conflict(user_id,usage_type,usage_date) do update
    set count = public.usage_counters.count + 1
    where public.usage_counters.count < p_limit
  returning count into new_count;
  if new_count is null then return 0; end if;
  return new_count;
end; $$;
revoke all on function public.consume_coach_quota(uuid,integer) from public,anon,authenticated;
grant execute on function public.consume_coach_quota(uuid,integer) to service_role;

-- Search respects invoker RLS; callers can retrieve only published chunks included in their tier.
create or replace function public.search_management_knowledge(p_query text, p_limit integer default 5)
returns table(title text, content text, source_url text)
language sql stable security invoker set search_path = '' as $$
  select c.title,c.content,c.source_url
  from public.document_chunks c
  where c.is_published = true
    and c.content_tsv @@ pg_catalog.websearch_to_tsquery('english'::regconfig, coalesce(p_query,''))
  order by ts_rank(c.content_tsv, pg_catalog.websearch_to_tsquery('english'::regconfig, coalesce(p_query,''))) desc
  limit greatest(1, least(coalesce(p_limit,5),10));
$$;
revoke all on function public.search_management_knowledge(text,integer) from public,anon;
grant execute on function public.search_management_knowledge(text,integer) to authenticated;

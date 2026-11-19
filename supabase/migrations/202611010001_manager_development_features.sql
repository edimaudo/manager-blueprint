-- Manager Blueprint: capability progress and persistent AI coaching practice.
-- Apply after 202610250001_initial_schema.sql.

alter table public.user_goals
  add column if not exists capability_slug text;

create table if not exists public.capability_progress (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  capability_slug text not null,
  step text not null check (step in ('learn','apply','practice','assess')),
  status text not null default 'completed' check (status in ('not_started','in_progress','completed')),
  self_rating smallint check (self_rating between 1 and 5),
  reflection text not null default '' check (char_length(reflection) <= 6000),
  next_action text not null default '' check (char_length(next_action) <= 2000),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(user_id, capability_slug, step)
);
create index if not exists capability_progress_user_updated
  on public.capability_progress(user_id, updated_at desc);

create table if not exists public.coaching_sessions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  title text not null default 'Management coaching' check (char_length(title) <= 180),
  capability text not null default 'general' check (char_length(capability) <= 80),
  mode text not null default 'coach' check (mode in ('coach','roleplay','feedback')),
  scenario_slug text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists coaching_sessions_user_updated
  on public.coaching_sessions(user_id, updated_at desc);

create table if not exists public.coaching_messages (
  id uuid primary key default gen_random_uuid(),
  session_id uuid not null references public.coaching_sessions(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  role text not null check (role in ('user','model')),
  content text not null check (char_length(content) <= 12000),
  created_at timestamptz not null default now()
);
create index if not exists coaching_messages_session_created
  on public.coaching_messages(session_id, created_at);

alter table public.capability_progress enable row level security;
alter table public.coaching_sessions enable row level security;
alter table public.coaching_messages enable row level security;

revoke all on public.capability_progress, public.coaching_sessions, public.coaching_messages from anon;
revoke all on public.capability_progress, public.coaching_sessions, public.coaching_messages from authenticated;
grant select,insert,update,delete on public.capability_progress to authenticated;
grant select,insert,update,delete on public.coaching_sessions to authenticated;
grant select,insert,delete on public.coaching_messages to authenticated;

create policy capability_progress_own_all on public.capability_progress
  for all to authenticated using ((select auth.uid())=user_id)
  with check ((select auth.uid())=user_id);

create policy coaching_sessions_own_all on public.coaching_sessions
  for all to authenticated using ((select auth.uid())=user_id)
  with check ((select auth.uid())=user_id);

create policy coaching_messages_own_select on public.coaching_messages
  for select to authenticated using (
    (select auth.uid())=user_id and exists (
      select 1 from public.coaching_sessions s
      where s.id=coaching_messages.session_id and s.user_id=(select auth.uid())
    )
  );
create policy coaching_messages_own_insert on public.coaching_messages
  for insert to authenticated with check (
    (select auth.uid())=user_id and exists (
      select 1 from public.coaching_sessions s
      where s.id=coaching_messages.session_id and s.user_id=(select auth.uid())
    )
  );
create policy coaching_messages_own_delete on public.coaching_messages
  for delete to authenticated using ((select auth.uid())=user_id);

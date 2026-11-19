-- Manager Blueprint: development measurement, follow-up actions, reviews, and structured practice.
-- Apply after 202610250001_initial_schema.sql and 202611010001_manager_development_features.sql.

-- Selected development goals need a lifecycle, not just a selected/not-selected state.
alter table public.user_goals
  add column if not exists status text not null default 'active'
    check (status in ('active','on_hold','completed')),
  add column if not exists target_date date,
  add column if not exists updated_at timestamptz not null default now();

-- Append-only follow-up assessments. The onboarding baseline remains in baseline_assessments.
create table if not exists public.capability_assessments (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  capability_slug text not null,
  ratings jsonb not null default '{}'::jsonb,
  overall_score numeric(3,2) not null check (overall_score between 1 and 5),
  evidence text not null default '' check (char_length(evidence) <= 6000),
  reflection text not null default '' check (char_length(reflection) <= 6000),
  next_action text not null default '' check (char_length(next_action) <= 2000),
  practice_attempt_id uuid,
  created_at timestamptz not null default now()
);
create index if not exists capability_assessments_user_cap_created
  on public.capability_assessments(user_id, capability_slug, created_at desc);

-- Concrete commitments generated from assessments, practice debriefs, and monthly reviews.
create table if not exists public.development_actions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  capability_slug text not null,
  title text not null check (char_length(title) between 1 and 240),
  detail text not null default '' check (char_length(detail) <= 3000),
  source_type text not null default 'manual' check (source_type in ('assessment','practice','review','manual')),
  source_id uuid,
  status text not null default 'open' check (status in ('open','in_progress','completed','dismissed')),
  due_date date,
  completed_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists development_actions_user_status_due
  on public.development_actions(user_id, status, due_date, created_at desc);

-- A lightweight periodic reflection on goals, progress, blockers, and next focus.
create table if not exists public.development_reviews (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  period_start date not null,
  period_end date not null,
  wins text not null default '' check (char_length(wins) <= 6000),
  barriers text not null default '' check (char_length(barriers) <= 6000),
  next_focus text not null default '' check (char_length(next_focus) <= 2000),
  next_review_on date not null,
  created_at timestamptz not null default now(),
  check (period_end >= period_start)
);
create index if not exists development_reviews_user_created
  on public.development_reviews(user_id, created_at desc);

-- Store the capability chosen for the next review focus, rather than guessing from the user's top goal.
alter table public.development_reviews
  add column if not exists next_focus_capability_slug text;

-- One practice attempt per scenario session. Repeating a scenario creates a new row linked to the prior attempt.
alter table public.coaching_sessions
  add column if not exists difficulty text not null default 'applied'
    check (difficulty in ('foundation','applied','advanced'));

create table if not exists public.practice_attempts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  session_id uuid not null unique references public.coaching_sessions(id) on delete cascade,
  parent_attempt_id uuid references public.practice_attempts(id) on delete set null,
  capability_slug text not null,
  scenario_slug text not null,
  difficulty text not null default 'applied' check (difficulty in ('foundation','applied','advanced')),
  criteria jsonb not null default '[]'::jsonb,
  status text not null default 'in_progress' check (status in ('in_progress','debriefed')),
  debrief jsonb not null default '{}'::jsonb,
  overall_score numeric(3,2) check (overall_score between 1 and 5),
  created_at timestamptz not null default now(),
  completed_at timestamptz
);
create index if not exists practice_attempts_user_cap_created
  on public.practice_attempts(user_id, capability_slug, created_at desc);

alter table public.capability_assessments
  add constraint capability_assessments_practice_attempt_fk
  foreign key (practice_attempt_id) references public.practice_attempts(id) on delete set null;

-- RLS: every new record is private to its owning user. No anon access.
alter table public.capability_assessments enable row level security;
alter table public.development_actions enable row level security;
alter table public.development_reviews enable row level security;
alter table public.practice_attempts enable row level security;

revoke all on public.capability_assessments, public.development_actions,
  public.development_reviews, public.practice_attempts from anon;
revoke all on public.capability_assessments, public.development_actions,
  public.development_reviews, public.practice_attempts from authenticated;

grant select, insert on public.capability_assessments to authenticated;
grant select, insert, update, delete on public.development_actions to authenticated;
grant select, insert on public.development_reviews to authenticated;
grant select, insert, update on public.practice_attempts to authenticated;
grant update on public.user_goals to authenticated;

create policy capability_assessments_own_all on public.capability_assessments
  for all to authenticated using ((select auth.uid())=user_id)
  with check ((select auth.uid())=user_id);
create policy development_actions_own_all on public.development_actions
  for all to authenticated using ((select auth.uid())=user_id)
  with check ((select auth.uid())=user_id);
create policy development_reviews_own_all on public.development_reviews
  for all to authenticated using ((select auth.uid())=user_id)
  with check ((select auth.uid())=user_id);
create policy practice_attempts_own_all on public.practice_attempts
  for all to authenticated using ((select auth.uid())=user_id)
  with check ((select auth.uid())=user_id);

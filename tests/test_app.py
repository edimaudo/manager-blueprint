import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('APP_ENCRYPTION_KEY','MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA=')
from fastapi.testclient import TestClient
from app import app, STYLE_QUESTIONS, COACH_QUIZ, TOOLS, can_access_tool

def test_landing_page_uses_welcome_copy_and_keeps_access_choices_in_product_flow():
    c=TestClient(app)
    r=c.get('/')
    assert r.status_code==200
    assert 'A personalized development plan for managers.' in r.text
    assert 'Create Your Manager Blueprint' in r.text and 'See how it works' in r.text
    assert 'Sign In' not in r.text
    assert 'Manager Plus' not in r.text and 'Manager Pro' not in r.text

def test_admin_login_has_separate_route():
    r=TestClient(app).get('/admin/login')
    assert r.status_code==200 and 'Administrator sign in' in r.text

def test_style_question_count_and_coach_quiz():
    from collections import Counter
    assert len(STYLE_QUESTIONS)==32
    assert Counter(item["scale"] for item in STYLE_QUESTIONS)=={"d":4,"i":4,"s":4,"c":4,"ex":4,"in":4,"re":4,"st":4}
    assert len(COACH_QUIZ)==5

def test_health_does_not_require_credentials():
    r=TestClient(app).get('/health')
    assert r.status_code==200 and r.json()=={'status':'ok'}


def test_resource_entitlements_are_tiered():
    assert can_access_tool("one-to-one-agenda", "free")
    assert not can_access_tool("feedback-planner", "free")
    assert can_access_tool("feedback-planner", "plus")
    assert not can_access_tool("skip-level-planner", "plus")
    assert can_access_tool("skip-level-planner", "pro")


def test_capability_catalogue_is_complete_and_linked():
    from content_catalog import CAPABILITIES, SCENARIOS, RESOURCES, GOAL_TO_CAPABILITY
    from jinja2 import Environment, FileSystemLoader
    root = Path(__file__).resolve().parents[1]
    resource_ids = {item['id'] for item in RESOURCES}
    tool_source = (root / 'app.py').read_text()
    # Every capability has all four development stages and working catalogue references.
    assert len(CAPABILITIES) == 18
    for slug, item in CAPABILITIES.items():
        assert item['domain'] in {'yourself', 'others', 'up'}
        assert len(item['learn']) >= 3
        assert len(item['assess']) >= 3
        assert item['scenario'] in SCENARIOS
        assert item['resource_ids']
        assert set(item['resource_ids']).issubset(resource_ids)
    assert all(slug in CAPABILITIES for slug in GOAL_TO_CAPABILITY.values())
    capability_scenarios = [item['scenario'] for item in CAPABILITIES.values()]
    assert len(capability_scenarios) == len(set(capability_scenarios))
    assert all(SCENARIOS[scenario]['capability'] in CAPABILITIES for scenario in capability_scenarios)
    # Compile every template to catch Jinja syntax errors before deployment.
    env = Environment(loader=FileSystemLoader(str(root / 'templates')))
    for template in env.list_templates():
        env.get_template(template)


def test_starter_resources_only_use_requested_publishers():
    from content_catalog import RESOURCES
    hosts = {item['url'].split('/')[2].lower() for item in RESOURCES}
    assert hosts == {'monday.com', 'asana.com', 'ticktick.com', 'help.ticktick.com'}
    assert any('project-collaboration' in item['url'] for item in RESOURCES)
    assert any(item['url'] == 'https://asana.com/resources/category/team-growth' for item in RESOURCES)
    assert any(item['url'] == 'https://ticktick.com/resources' for item in RESOURCES)
    assert all(item.get('summary') and item.get('capabilities') for item in RESOURCES)


def test_style_questions_api_returns_original_32_statement_likert_profile(monkeypatch):
    import app as app_module
    async def fake_current_user(request, required=True):
        return {"id":"00000000-0000-0000-0000-000000000001","_access_token":"test"}
    monkeypatch.setattr(app_module,"current_user",fake_current_user)
    response=TestClient(app_module.app).get("/api/style/questions")
    assert response.status_code==200
    payload=response.json()
    assert len(payload["questions"])==32
    assert len(payload["scale"])==5
    assert {item["section"] for item in payload["questions"]}=={"behaviour","contribution"}
    assert "not an official" in payload["note"]


def test_management_style_neutral_answers_produce_midpoint_scores():
    from content_catalog import score_management_style
    result=score_management_style({str(i):"3" for i in range(1,33)})
    assert set(result["disc_percentages"].values())=={50}
    assert set(result["strength_domain_percentages"].values())=={50}


def test_management_style_profile_scores_eight_dimensions_and_blended_patterns():
    from content_catalog import score_management_style, STYLE_QUESTIONS
    answers={str(i):"3" for i in range(1,33)}
    # D leads slightly over i; executing leads slightly over influencing.
    for idx,value in zip(range(1,5),["5","4","4","2"]): answers[str(idx)]=value
    for idx,value in zip(range(5,9),["4","4","4","2"]): answers[str(idx)]=value
    for idx,value in zip(range(17,21),["5","4","4","2"]): answers[str(idx)]=value
    for idx,value in zip(range(21,25),["4","4","4","2"]): answers[str(idx)]=value
    result=score_management_style(answers)
    assert result["assessment_version"]==2
    assert result["supporting_styles"]==["d","i"]
    assert result["top_strength_domains"]==["ex","in"]
    assert result["archetype"]=="Outcome Driver"
    assert set(result["disc_percentages"])=={"d","i","s","c"}
    assert set(result["strength_domain_percentages"])=={"ex","in","re","st"}
    assert all(0 <= score <= 100 for score in result["disc_percentages"].values())
    assert all(0 <= score <= 100 for score in result["strength_domain_percentages"].values())
    assert result["management_approach"]
    assert "not an official DiSC or CliftonStrengths assessment" in result["disclaimer"]
    assert len(STYLE_QUESTIONS)==32


def test_recommendations_consider_goals_baseline_and_progress():
    from content_catalog import recommend_capabilities
    goals = [{'capability_slug':'delegation','priority':3}]
    baseline = {'capability_scores':{'delegation':2,'feedback':1,'prioritization':4}}
    progress = [
        {'capability_slug':'delegation','step':'learn','status':'completed'},
        {'capability_slug':'delegation','step':'apply','status':'completed'},
        {'capability_slug':'feedback','step':'learn','status':'completed'},
        {'capability_slug':'feedback','step':'apply','status':'completed'},
        {'capability_slug':'feedback','step':'practice','status':'completed'},
    ]
    recommended = recommend_capabilities(goals, baseline, progress)
    assert 'delegation' in recommended
    assert 'feedback' in recommended
    assert len(recommended) == 3


def test_new_routes_are_registered():
    paths = {route.path for route in app.routes}
    assert '/capability/{slug}' in paths
    assert '/capability/{slug}/progress' in paths
    assert '/api/coach/sessions' in paths
    assert '/api/coach/sessions/{session_id}' in paths


def test_coaching_context_uses_full_blueprint_and_preference(monkeypatch):
    import asyncio
    import app as manager_app

    async def fake_db_get(table, user, query='select=*'):
        data = {
            'profiles': [{'management_stage':'first_time','display_name':'Test Manager'}],
            'user_goals': [{'domain':'others','capability':'Delegation','capability_slug':'delegation','priority':1}],
            'baseline_assessments': [{'result': {'capability_scores': {'delegation':2}, 'domain_scores': {'others':2.8}}}],
            'style_assessments': [{'result': {'archetype':'Driver · Execution'}}],
            'coach_preferences': [{'result': {'recommended_coach':'Action-oriented'}}],
            'coaching_diary': [{'entry':'I avoided a difficult delegation conversation.','next_step':'Clarify decision rights.'}],
            'capability_progress': [{'capability_slug':'delegation','step':'practice','status':'in_progress','reflection':'Practised setting an outcome.'}],
        }
        return data.get(table, [])

    async def fake_request_json(*args, **kwargs):
        if args and args[0] == 'POST' and 'search_management_knowledge' in str(args[1]):
            return [{'title':'Delegation guide','content':'Clarify outcome and authority.','source_url':'https://example.test/guide'}]
        return []

    monkeypatch.setattr(manager_app, 'db_get', fake_db_get)
    monkeypatch.setattr(manager_app, 'request_json', fake_request_json)
    monkeypatch.setattr(manager_app, 'supa_headers', lambda *args, **kwargs: {})
    context = asyncio.run(manager_app.get_context({'id':'00000000-0000-0000-0000-000000000001','_access_token':'test'}, 'delegation', 'How do I delegate?'))
    for expected in ('first_time','Delegation','capability_scores','Driver','Action-oriented','action-focused','Clarify decision rights','Delegation guide','monday.com','asana.com'):
        assert expected in context


def test_blueprint_renders_legacy_baseline_without_new_fields():
    from jinja2 import Environment, FileSystemLoader
    root = Path(__file__).resolve().parents[1]
    env = Environment(loader=FileSystemLoader(str(root / 'templates')))
    template = env.get_template('blueprint.html')
    html = template.render(
        user={'app_metadata':{}}, profile={'management_stage':'first_time'}, goals=[], style=None,
        baseline={'created_at':'2026-01-01T00:00:00Z','result':{'domain_scores':{'yourself':3,'others':3,'up':3},'recommended_start':'others'}},
        diary=[], tier='free', capabilities={'yourself':[],'others':[],'up':[]}, recommendations=[],
        progress_by_cap={}, completion={}, overall_progress=0, completed_stages=0, total_stages=72, next_actions=[]
    )
    assert 'Your starting point' in html
    assert 'Development opportunities' not in html
    assert 'Your next actions' in html


def test_followup_assessment_averages_three_capability_indicators():
    from app import score_followup_ratings
    from content_catalog import CAPABILITIES
    indicators = CAPABILITIES['delegation']['assess']
    ratings, score = score_followup_ratings({'q1':'3','q2':'4','q3':'5'}, indicators)
    assert len(ratings) == 3
    assert score == 4.0
    assert ratings['2']['indicator'] == indicators[1]
    import pytest
    with pytest.raises(ValueError):
        score_followup_ratings({'q1':'3','q2':'9','q3':'5'}, indicators)


def test_every_practice_scenario_has_capability_specific_evaluation_criteria():
    from app import scenario_evaluation_criteria
    from content_catalog import CAPABILITIES, SCENARIOS
    assert len(SCENARIOS) == len(CAPABILITIES)
    for scenario_slug, scenario in SCENARIOS.items():
        rubric = scenario_evaluation_criteria(scenario_slug)
        assert len(rubric) == 5
        capability = CAPABILITIES[scenario['capability']]
        assert [item['focus'] for item in rubric[:3]] == capability['assess']
        assert rubric[3]['name'] == 'Listening and inquiry'
        assert rubric[4]['name'] == 'Clarity and follow-through'


def test_structured_practice_debrief_is_validated_against_fixed_rubric():
    import json
    from app import normalize_practice_debrief
    rubric = [
        {'name':'Capability indicator 1','focus':'Clarifies outcomes.'},
        {'name':'Listening and inquiry','focus':'Asks relevant questions.'},
    ]
    raw = json.dumps({
        'overall_summary':'The manager clarified the outcome and explored the concern.',
        'criteria':[
            {'name':'Capability indicator 1','score':4,'evidence':'The manager stated the expected result.'},
            {'name':'Listening and inquiry','score':3,'evidence':'The manager asked one useful question.'},
            {'name':'Unexpected criterion','score':5,'evidence':'Must be ignored.'},
        ],
        'strengths':['Clarified the expected outcome.'],
        'improvement_areas':['Explore the counterpart concern in more depth.'],
        'stronger_language':['What is the main risk you see?'],
        'next_actions':['Agree an interim checkpoint.'],
        'reflection_question':'What information did you still need?'
    })
    result = normalize_practice_debrief(raw, rubric)
    assert result['overall_score'] == 3.5
    assert len(result['criteria']) == 2
    assert result['criteria'][0]['score'] == 4
    assert result['criteria'][1]['score'] == 3
    assert all(item['name'] != 'Unexpected criterion' for item in result['criteria'])
    assert normalize_practice_debrief('not json', rubric) is None


def test_practice_attempt_comparison_matches_criteria_and_difficulty():
    from app import _practice_comparison
    attempts = [
        {'id':'new','status':'debriefed','difficulty':'applied','created_at':'2026-11-02T10:00:00Z',
         'overall_score':4.0,'debrief':{'criteria':[{'name':'Listening','score':4},{'name':'Clarity','score':4}]}},
        {'id':'old','status':'debriefed','difficulty':'applied','created_at':'2026-10-20T10:00:00Z',
         'overall_score':3.0,'debrief':{'criteria':[{'name':'Listening','score':2},{'name':'Clarity','score':4}]}},
        {'id':'open','status':'in_progress','difficulty':'advanced','created_at':'2026-11-03T10:00:00Z','debrief':{}},
    ]
    comparison = _practice_comparison(attempts)
    assert comparison['latest']['id'] == 'new'
    assert comparison['previous']['id'] == 'old'
    assert comparison['same_difficulty'] is True
    assert comparison['criteria'][0]['delta'] == 2


def test_new_development_routes_and_tables_are_present():
    paths = {route.path for route in app.routes}
    assert '/capability/{slug}/assessment' in paths
    assert '/goals/{goal_id}/update' in paths
    assert '/development-actions/{action_id}/update' in paths
    assert '/development/review' in paths
    migration = (Path(__file__).resolve().parents[1] / 'supabase/migrations/202611020001_progress_and_practice.sql').read_text()
    for table in ('capability_assessments','development_actions','development_reviews','practice_attempts'):
        assert f'create table if not exists public.{table}' in migration
        assert f'alter table public.{table} enable row level security' in migration


def test_capability_page_contains_repeatable_assessment_and_practice_comparison():
    from jinja2 import Environment, FileSystemLoader
    from content_catalog import CAPABILITIES
    from app import scenario_evaluation_criteria
    root = Path(__file__).resolve().parents[1]
    env = Environment(loader=FileSystemLoader(str(root / 'templates')))
    template = env.get_template('capability.html')
    slug = 'delegation'
    capability = CAPABILITIES[slug]
    html = template.render(
        user={'app_metadata':{}}, slug=slug, capability=capability,
        progress={}, baseline_score=2, assessment_history=[{'label':'Starting baseline','score':2,'created_at':'2026-01-01','kind':'baseline'}],
        latest_assessment=None, assessments=[], selected_goal=True, resources=[], scenario={'title':'Scenario','brief':'Brief','role':'Employee'},
        scenario_slug=capability['scenario'], scenario_criteria=scenario_evaluation_criteria(capability['scenario']),
        tool=None, tool_allowed=False, practice_attempts=[], latest_debriefed=None, practice_comparison=None
    )
    assert 'Save follow-up assessment' in html
    assert 'name="q1"' in html and 'name="q2"' in html and 'name="q3"' in html
    assert 'Your development trend' in html
    assert 'Evaluation criteria' in html


def test_followup_assessment_history_keeps_baseline_and_chronological_scores():
    from app import _assessment_history
    history = _assessment_history(
        {'score': 2.0, 'created_at': '2026-01-01T00:00:00Z'},
        [
            {'overall_score': 4.0, 'created_at': '2026-03-01T00:00:00Z'},
            {'overall_score': 3.0, 'created_at': '2026-02-01T00:00:00Z'},
        ],
    )
    assert [item['kind'] for item in history] == ['baseline', 'follow_up', 'follow_up']
    assert [item['score'] for item in history] == [2.0, 3.0, 4.0]


def test_practice_difficulty_levels_have_distinct_guidance():
    from app import PRACTICE_DIFFICULTIES
    assert set(PRACTICE_DIFFICULTIES) == {'foundation', 'applied', 'advanced'}
    instructions = [PRACTICE_DIFFICULTIES[key]['instruction'] for key in ('foundation', 'applied', 'advanced')]
    assert len(set(instructions)) == 3
    assert 'reasonably receptive' in instructions[0]
    assert 'competing priority' in instructions[1]
    assert 'multiple stakeholder' in instructions[2]


def test_development_review_renders_commitments_and_completed_actions():
    from jinja2 import Environment, FileSystemLoader
    root = Path(__file__).resolve().parents[1]
    env = Environment(loader=FileSystemLoader(str(root / 'templates')))
    template = env.get_template('development_review.html')
    html = template.render(
        user={'app_metadata': {}}, goals=[{'capability':'Delegation','status':'active','target_date':'2026-12-01'}],
        assessments=[{'capability_slug':'delegation','overall_score':3.5,'created_at':'2026-11-01'}],
        attempts=[{'capability_slug':'delegation','scenario_slug':'delegation_missed_deadline','difficulty':'applied','overall_score':4.0,'status':'debriefed','created_at':'2026-11-01'}],
        open_actions=[{'capability_slug':'delegation','title':'Clarify decision rights','detail':'Discuss the next assignment.','status':'in_progress','due_date':'2026-11-10'}],
        completed_actions=[{'title':'Schedule a 1:1','completed_at':'2026-10-20','updated_at':'2026-10-20'}],
        reviews=[], capabilities={}, period_start='2026-10-01', next_review_on='2026-12-02'
    )
    assert 'Development commitments' in html
    assert 'Clarify decision rights' in html
    assert 'Due 2026-11-10' in html
    assert 'Schedule a 1:1' in html


def test_planner_download_language_is_not_worksheet_language():
    from jinja2 import Environment, FileSystemLoader
    root = Path(__file__).resolve().parents[1]
    env = Environment(loader=FileSystemLoader(str(root / 'templates')))
    html = env.get_template('tool.html').render(
        user={'app_metadata': {}}, tool={'title':'Delegation planner','category':'Managing Others','description':'Plan a delegation conversation.','fields':[('outcome','Desired outcome')]},
        slug='delegation-planner', tier='free', capability_slug='delegation'
    )
    assert 'Download plan' in html
    assert 'worksheet' not in html.lower()


def test_progress_and_practice_migration_is_documented_in_sequence():
    readme = (Path(__file__).resolve().parents[1] / 'README.md').read_text()
    first = readme.index('202610250001_initial_schema.sql')
    second = readme.index('202611010001_manager_development_features.sql')
    third = readme.index('202611020001_progress_and_practice.sql')
    assert first < second < third



def test_next_capability_activity_follows_learn_apply_practice_assess_order():
    from app import next_capability_activity
    assert next_capability_activity({})['step'] == 'learn'
    assert next_capability_activity({'learn': {'status':'completed'}})['step'] == 'apply'
    assert next_capability_activity({'learn': {'status':'completed'}, 'apply': {'status':'in_progress'}})['step'] == 'apply'
    assert next_capability_activity({'learn': {'status':'completed'}, 'apply': {'status':'completed'}, 'practice': {'status':'completed'}})['step'] == 'assess'
    result = next_capability_activity({step: {'status':'completed'} for step in ('learn','apply','practice','assess')})
    assert result['step'] == 'review'


def test_blueprint_recommendation_displays_next_activity():
    from jinja2 import Environment, FileSystemLoader
    root = Path(__file__).resolve().parents[1]
    env = Environment(loader=FileSystemLoader(str(root / 'templates')))
    html = env.get_template('blueprint.html').render(
        user={'app_metadata':{}}, profile={'management_stage':'first_time'}, goals=[], style=None, baseline=None,
        diary=[], tier='free', capabilities={'yourself':[],'others':[],'up':[]},
        recommendations=[{'slug':'delegation','domain_label':'Managing Others','title':'Delegation','summary':'Clarify ownership.',
                          'completed':1,'latest_score':2.5,'next_step':'practice','next_step_label':'Practice',
                          'next_step_description':'Practise the mapped management scenario.'}],
        progress_by_cap={}, completion={}, overall_progress=0, completed_stages=0, total_stages=72,
        development_actions=[], completed_actions=[], last_review=None, review_due=True
    )
    assert 'Next activity: Practice' in html
    assert 'Continue with Delegation' in html


def test_billing_catalogue_is_provider_neutral_and_preserves_independent_paths():
    from app import BILLING_PRODUCTS, PAYMENT_PROVIDER
    assert BILLING_PRODUCTS["manager_plus"]["kind"] == "subscription"
    assert BILLING_PRODUCTS["manager_pro"]["kind"] == "subscription"
    assert all(BILLING_PRODUCTS[key]["kind"] == "payment" for key in (
        "delegation_toolkit", "feedback_toolkit", "stakeholder_toolkit", "performance_toolkit"))
    assert all("price_env" not in item for item in BILLING_PRODUCTS.values())
    assert PAYMENT_PROVIDER.enabled is False
    assert PAYMENT_PROVIDER.name == "not_configured"


def test_billing_routes_are_placeholders_without_a_provider(monkeypatch):
    import app as app_module
    async def fake_current_user(request, required=True):
        return {"id":"00000000-0000-0000-0000-000000000001","email":"manager@example.test","_access_token":"test"}
    monkeypatch.setattr(app_module,"current_user",fake_current_user)
    client=TestClient(app_module.app)
    checkout=client.post("/billing/checkout/manager_plus")
    assert checkout.status_code==503
    assert "No payment has been initiated or charged" in checkout.json()["detail"]
    portal=client.post("/billing/portal")
    assert portal.status_code==503
    assert "payment provider is selected" in portal.json()["detail"]


def test_pricing_and_billing_pages_are_registered_without_provider_webhooks():
    from app import app
    paths={route.path for route in app.routes}
    assert {"/pricing","/account/billing","/billing/checkout/{product_key}","/billing/portal"}.issubset(paths)
    assert "/webhooks/stripe" not in paths
    from jinja2 import Environment, FileSystemLoader
    env=Environment(loader=FileSystemLoader(str(Path(__file__).resolve().parents[1]/"templates")))
    for name in ("base.html","pricing.html","billing.html"):
        env.get_template(name)

def test_pricing_page_renders_with_disabled_provider_placeholders():
    response=TestClient(app).get('/pricing')
    assert response.status_code==200
    assert 'Start Free' in response.text
    assert 'Buy What You Need' in response.text
    assert 'Go Further' in response.text
    assert 'Subscriptions' in response.text
    assert 'Individual one-time purchases' in response.text
    assert 'Online payments are not enabled yet' not in response.text
    assert 'Not available yet' in response.text
    assert 'Stripe' not in response.text


def test_design_tokens_use_prd_palette_and_font_scale_values():
    root = Path(__file__).resolve().parents[1]
    css = (root / 'static/css/app.css').read_text()
    js = (root / 'static/js/app.js').read_text()
    assert '--brand-teal: #1B546B' in css
    assert '--brand-ice: #EBF6FA' in css
    assert '--primary: var(--brand-teal)' in css
    assert '--primary-soft: var(--brand-ice)' in css
    assert 'small: 0.75, medium: 1, large: 1.25' in js


def test_access_options_show_independent_paths():
    response = TestClient(app).get('/pricing')
    assert response.status_code == 200
    assert 'Start Free' in response.text
    assert 'Buy What You Need' in response.text
    assert 'Go Further' in response.text
    assert 'You do not need to make a one-time purchase before subscribing.' in response.text


def test_blueprint_keeps_billing_out_of_the_main_application():
    from jinja2 import Environment, FileSystemLoader
    root = Path(__file__).resolve().parents[1]
    env = Environment(loader=FileSystemLoader(str(root / 'templates')))
    template = env.get_template('blueprint.html')
    html = template.render(
        profile={'management_stage':'first_time'}, goals=[], style=None, baseline=None,
        capabilities={'yourself':[],'others':[],'up':[]}, recommendations=[],
        overall_progress=0, completed_stages=0, total_stages=72,
        development_actions=[], completed_actions=[], last_review=None,
        review_due=True, show_access=True
    )
    assert 'Access options' not in html
    assert 'Billing' not in html
    assert 'Choose how you want to continue' not in html
    assert 'Your Manager Blueprint sections' not in html  # tabs are progressively enhanced by JS


def test_monthly_quota_limits_match_product_access_rules():
    from app import monthly_limits
    assert monthly_limits('free') == {'tool': 1, 'article': 5}
    assert monthly_limits('plus') == {'tool': 3, 'article': None}
    assert monthly_limits('pro') == {'tool': None, 'article': None}


def test_style_validation_metrics_use_only_valid_32_item_opt_in_records():
    from app import style_validation_metrics
    from content_catalog import STYLE_QUESTIONS
    records = []
    for person in range(35):
        answers = {}
        for idx, item in enumerate(STYLE_QUESTIONS, start=1):
            # Produce variation while preserving valid five-point responses.
            value = 2 + ((person + idx) % 3)
            answers[str(idx)] = str(6-value if item.get('reverse') else value)
        records.append({'answers': answers, 'pilot_consent': True})
    records.append({'answers': {'1':'5'}, 'pilot_consent': True})
    result = style_validation_metrics(records)
    assert result['pilot_responses'] == 35
    assert result['sample_warning'].startswith('Exploratory pilot statistics')
    assert len(result['items']) == 32
    assert set(result['reliability_by_dimension']) == {'d','i','s','c','ex','in','re','st'}
    assert all(item['corrected_item_total_correlation'] is None or -1 <= item['corrected_item_total_correlation'] <= 1 for item in result['items'])
    assert 'do not establish validity' in result['method_note']


def test_style_validation_metrics_warn_when_pilot_sample_is_small():
    from app import style_validation_metrics
    result = style_validation_metrics([])
    assert result['pilot_responses'] == 0
    assert 'Fewer than 30' in result['sample_warning']
    assert all(item['cronbach_alpha'] is None for item in result['reliability_by_dimension'].values())


def test_quota_rpc_migration_is_atomic_and_service_role_only():
    from pathlib import Path
    migration = Path(__file__).resolve().parents[1] / 'supabase/migrations/202611120001_monthly_quotas_and_style_pilot.sql'
    sql = migration.read_text()
    assert 'on conflict (user_id, quota_key, period_start)' in sql.lower()
    assert 'where public.monthly_usage.usage_count < p_limit' in sql.lower()
    assert 'to service_role' in sql.lower()
    assert "add column if not exists pilot_consent boolean not null default false" in sql.lower()


def test_monthly_quota_consumption_calls_atomic_rpc_with_unique_item_key(monkeypatch):
    import asyncio
    import app as manager_app
    captured = {}
    async def fake_request_json(method, path, **kwargs):
        captured['method'] = method
        captured['path'] = path
        captured['body'] = kwargs['json_body']
        return {'allowed': True, 'used': 2, 'limit': 3, 'remaining': 1}
    monkeypatch.setattr(manager_app, 'request_json', fake_request_json)
    monkeypatch.setattr(manager_app, 'supa_headers', lambda **kwargs: {'role':'service'})
    result = asyncio.run(manager_app.consume_monthly_quota(
        {'id':'00000000-0000-0000-0000-000000000001'}, 'tool', 3, 'delegation-planner'))
    assert captured['method'] == 'POST'
    assert captured['path'] == '/rest/v1/rpc/consume_monthly_quota'
    assert captured['body']['p_item_key'] == 'delegation-planner'
    assert result['allowed'] is True and result['remaining'] == 1


def test_pilot_metrics_do_not_expose_participant_identifiers():
    from app import style_validation_metrics
    result = style_validation_metrics([{'user_id':'private-id','email':'private@example.com','answers':{}}])
    rendered = str(result)
    assert 'private-id' not in rendered
    assert 'private@example.com' not in rendered


def test_article_and_tool_quota_migration_counts_unique_items_and_resets_monthly():
    from pathlib import Path
    sql = (Path(__file__).resolve().parents[1] / 'supabase/migrations/202611120001_monthly_quotas_and_style_pilot.sql').read_text().lower()
    assert 'primary key (user_id, quota_key, period_start, item_key)' in sql
    assert "date_trunc('month', timezone('utc', now()))" in sql
    assert "already_counted" in sql


def test_health_and_authenticated_responses_include_security_headers():
    response=TestClient(app).get('/health')
    assert response.headers['x-content-type-options']=='nosniff'
    assert response.headers['x-frame-options']=='DENY'
    assert response.headers['referrer-policy']=='strict-origin-when-cross-origin'
    assert "frame-ancestors 'none'" in response.headers['content-security-policy']

def test_health_does_not_expose_model_or_vendor_configuration():
    payload=TestClient(app).get('/health').json()
    assert set(payload)=={'status'}
    assert 'model' not in payload and 'provider' not in payload

def test_production_configuration_fails_closed_when_secrets_or_hosts_missing(monkeypatch):
    import app as app_module
    monkeypatch.setattr(app_module,'APP_ENV','production')
    monkeypatch.setattr(app_module,'APP_BASE_URL','http://example.com')
    monkeypatch.setattr(app_module,'ALLOWED_HOSTS',[])
    monkeypatch.setattr(app_module,'ALLOWED_ORIGINS',{'http://example.com'})
    monkeypatch.setattr(app_module,'SUPABASE_URL','')
    monkeypatch.setattr(app_module,'SUPABASE_ANON_KEY','')
    monkeypatch.setattr(app_module,'SUPABASE_SERVICE_KEY','')
    monkeypatch.setattr(app_module,'FERNET_KEY','')
    monkeypatch.delenv('GOOGLE_API_KEY',raising=False)
    errors=app_module.production_configuration_errors()
    assert len(errors)>=8
    assert any('HTTPS' in item for item in errors)
    assert any('SUPABASE_SERVICE_ROLE_KEY' in item for item in errors)

def test_production_rejects_unsafe_requests_without_origin(monkeypatch):
    import app as app_module
    monkeypatch.setattr(app_module,'APP_ENV','production')
    response=TestClient(app_module.app).post('/logout')
    assert response.status_code==403

def test_cross_site_fetch_metadata_is_rejected(monkeypatch):
    import app as app_module
    response=TestClient(app_module.app).post('/logout',headers={'sec-fetch-site':'cross-site'})
    assert response.status_code==403

def test_request_body_size_limit_is_enforced():
    response=TestClient(app).post('/logout',headers={'content-length':str(23*1024*1024)})
    assert response.status_code==413


def test_landing_and_dashboard_remove_footer_and_upsell_copy():
    from jinja2 import Environment, FileSystemLoader
    root = Path(__file__).resolve().parents[1]
    landing = (root / 'index.html').read_text()
    assert '<footer' not in landing
    assert 'Build your Manager Blueprint.' not in landing
    env = Environment(loader=FileSystemLoader(str(root / 'templates')))
    html = env.get_template('blueprint.html').render(
        profile={'management_stage':'first_time'}, goals=[], style=None, baseline=None,
        capabilities={'yourself':[],'others':[],'up':[]}, recommendations=[],
        overall_progress=0, completed_stages=0, total_stages=72,
        development_actions=[], completed_actions=[], last_review=None,
        review_due=True, show_access=True
    )
    assert 'Access options' not in html and 'Billing' not in html
    assert 'Choose how you want to continue' not in html
    assert 'blueprint-tabs.js' in html


def test_assessment_has_domain_tabs_and_completion_progress():
    from jinja2 import Environment, FileSystemLoader
    from content_catalog import ASSESSMENT_QUESTIONS
    root = Path(__file__).resolve().parents[1]
    env = Environment(loader=FileSystemLoader(str(root / 'templates')))
    html = env.get_template('assessment.html').render(questions=ASSESSMENT_QUESTIONS)
    assert 'Managing Yourself' in html and 'Managing Others' in html and 'Managing Up' in html
    assert 'assessment-progress-fill' in html
    assert html.count('data-assessment-domain=') == 18

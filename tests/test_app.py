import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('APP_ENCRYPTION_KEY','MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA=')
from fastapi.testclient import TestClient
from app import app, STYLE_QUESTIONS, COACH_QUIZ, TOOLS, can_access_tool

def test_landing_page_has_three_plans_and_no_prices():
    c=TestClient(app)
    r=c.get('/')
    assert r.status_code==200
    assert 'Manager Plus' in r.text and 'Manager Pro' in r.text and 'Free' in r.text
    assert '$15' not in r.text and '$150' not in r.text

def test_admin_login_has_separate_route():
    r=TestClient(app).get('/admin/login')
    assert r.status_code==200 and 'Administrator sign in' in r.text

def test_style_question_count_and_coach_quiz():
    assert len(STYLE_QUESTIONS)==12
    assert len(COACH_QUIZ)==5

def test_health_does_not_require_credentials():
    r=TestClient(app).get('/health')
    assert r.status_code==200 and r.json()['model']=='gemini-3.6-flash'


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


def test_management_style_reflection_shows_close_patterns():
    from content_catalog import score_management_style
    answers = {
        '1':'d','2':'d','3':'i','4':'i','5':'s','6':'c',
        '7':'ex','8':'ex','9':'in','10':'in','11':'re','12':'st'
    }
    result = score_management_style(answers)
    assert result['supporting_styles'] == ['d', 'i']
    assert result['top_strength_domains'] == ['ex', 'in']
    assert 'Driver / Connector' in result['archetype']
    assert sum(result['disc_percentages'].values()) == 100
    assert sum(result['strength_domain_percentages'].values()) == 100
    assert result['management_approach']
    assert result['disclaimer'].startswith('This original developmental reflection')


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
    assert 'Your capability baseline' in html
    assert 'Development opportunities' not in html
    assert 'Actions to follow up' in html

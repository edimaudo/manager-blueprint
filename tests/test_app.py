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

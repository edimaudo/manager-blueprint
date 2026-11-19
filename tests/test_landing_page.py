import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('APP_ENCRYPTION_KEY', 'MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA=')
from fastapi.testclient import TestClient
from app import app


def test_landing_page_has_a_descriptive_product_headline_and_clear_actions():
    response = TestClient(app).get('/')
    assert response.status_code == 200
    assert 'A personalized development plan for managers.' in response.text
    assert 'Understand your management style' in response.text
    assert 'Create Your Manager Blueprint' in response.text
    assert 'See how it works' in response.text
    assert 'Sign In' not in response.text


def test_landing_page_is_concise_and_does_not_reintroduce_rejected_sections():
    response = TestClient(app).get('/')
    for removed_phrase in (
        'Learn it. Apply it. Practise it. Reflect on it.',
        'Start with the situations that matter to you.',
        'Managing Yourself',
        'Managing Others',
        'Managing Up',
        'MANAGER DEVELOPMENT, MADE PRACTICAL',
        'A PERSONALIZED STARTING POINT',
        'BUILT AROUND REAL MANAGEMENT WORK',
        'YOUR DEVELOPMENT, MADE CLEAR',
    ):
        assert removed_phrase not in response.text


def test_landing_page_uses_the_manager_blueprint_product_visual():
    response = TestClient(app).get('/')
    for phrase in (
        'Your Manager Blueprint',
        'First-Time Manager',
        'Strengths',
        'Development opportunities',
        'Build a stronger delegation approach',
    ):
        assert phrase in response.text


def test_eyebrow_labels_are_removed_from_all_application_templates():
    root = Path(__file__).resolve().parents[1]
    sources = list((root / 'templates').glob('*.html')) + [root / 'index.html']
    for source in sources:
        markup = source.read_text()
        assert 'class="eyebrow"' not in markup, source.name
        assert 'class="eyebrow ' not in markup, source.name


def test_application_styles_use_the_prd_brand_palette():
    root = Path(__file__).resolve().parents[1]
    for stylesheet in ('static/css/app.css', 'static/css/landing.css'):
        css = (root / stylesheet).read_text().upper()
        for color in ('#1B546B', '#EBF6FA', '#C6E5F1', '#A1D4E8', '#7CC3DE', '#58B2D5', '#33A1CC', '#2A84A7', '#216783', '#0E2D39', '#051014'):
            assert color in css, f'{color} missing from {stylesheet}'
        assert '#385767' not in css
        assert '#F6FBFD' not in css

def test_dark_mode_uses_sky_blue_on_neutral_charcoal_surfaces_across_the_app():
    root = Path(__file__).resolve().parents[1]
    app_css = (root / 'static/css/app.css').read_text()
    landing_css = (root / 'static/css/landing.css').read_text()
    app_dark = app_css.split('[data-theme="dark"] {', 1)[1].split('}', 1)[0]
    landing_dark = landing_css.split('[data-theme="dark"] {', 1)[1].split('}', 1)[0]

    for token in (
        '--primary: #58B2D5',
        '--primary-strong: #F1F6F8',
        '--primary-soft: #243E49',
        '--background: #171C20',
        '--surface: #22292E',
        '--surface-alt: #2C353B',
        '--border: #46545B',
        '--button-text: #051014',
        '--primary-hover: #33A1CC',
    ):
        assert token in app_dark, token

    for token in (
        '--primary: #58B2D5',
        '--primary-strong: #F1F6F8',
        '--primary-soft: #243E49',
        '--bg: #171C20',
        '--surface: #22292E',
        '--border: #46545B',
        '--button-text: #051014',
        '--primary-hover: #33A1CC',
    ):
        assert token in landing_dark, token

    assert '#0B1D2A' not in app_dark + landing_dark
    assert '#4F9BC2' not in app_dark + landing_dark


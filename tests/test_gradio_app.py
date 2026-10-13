"""
Unit tests for Gradio application construction and tab verification.
"""

from app import build_app

def test_gradio_app_structure():
    demo = build_app()
    assert demo is not None
    # Verify title
    assert demo.title == "GenAI Video Intelligence Studio"

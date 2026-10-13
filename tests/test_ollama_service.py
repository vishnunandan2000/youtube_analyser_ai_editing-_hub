"""
Unit tests for Ollama service health checking and bounded JSON repair.
"""

from services.ollama_service import ollama_service

def test_ollama_json_repair():
    # Test repairing JSON wrapped in markdown backticks
    raw_markdown_json = '```json\n{"status": "success", "score": 95}\n```'
    parsed = ollama_service._repair_and_parse_json(raw_markdown_json)
    assert parsed is not None
    assert parsed.get("status") == "success"
    assert parsed.get("score") == 95

def test_ollama_array_repair():
    raw_array = '[{"id": 1, "text": "Segment A"}, {"id": 2, "text": "Segment B"}]'
    parsed = ollama_service._repair_and_parse_json(raw_array)
    assert parsed is not None
    items = parsed if isinstance(parsed, list) else parsed.get("items", [])
    assert len(items) == 2
    assert items[0]["id"] == 1


def test_ollama_health_structure():
    health = ollama_service.check_health()
    assert "status" in health
    assert "base_url" in health
    assert "configured_model" in health
    assert "model_ready" in health

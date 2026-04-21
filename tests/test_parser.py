import pytest
from core.parser import repair_json, extract_tool_calls

def test_repair_json():
    # Test single quotes to double quotes
    bad_json = "{'tool': 'read', 'args': {'path': 'test.py'}}"
    fixed = repair_json(bad_json)
    assert '"tool": "read"' in fixed
    assert '"path": "test.py"' in fixed

def test_extract_tool_calls_markdown():
    text = "Here is the call:\n```json\n{\"tool\": \"list\", \"args\": {}}\n```"
    calls = extract_tool_calls(text)
    assert len(calls) == 1
    assert calls[0]["tool"] == "list"

def test_extract_tool_calls_raw():
    text = "Call this: {\"tool\": \"mkdir\", \"args\": {\"path\": \"new_dir\"}}"
    calls = extract_tool_calls(text)
    assert len(calls) == 1
    assert calls[0]["tool"] == "mkdir"

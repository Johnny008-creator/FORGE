#!/usr/bin/env python3
"""Test all new Forge features"""
import forge
import json

print("=" * 60)
print("FORGE v0.6.0+ UPGRADE TEST SUITE")
print("=" * 60)

# Test 1: Execution modes
print("\n[1] EXECUTION MODES")
print(f"  Initial mode: {forge.EXEC_MODE}")
forge.EXEC_MODE = "auto"
print(f"  After /auto: {forge.EXEC_MODE}")
print(f"  should_confirm('shell'): {forge.should_confirm('shell')}")
forge.EXEC_MODE = "ask"
print(f"  After /ask: {forge.EXEC_MODE}")
print(f"  should_confirm('shell'): {forge.should_confirm('shell')}")
print(f"  should_confirm('read'): {forge.should_confirm('read')}")

# Test 2: Tool parsing — Strategy 1 (JSON)
print("\n[2] TOOL PARSING — JSON")
json_text = '{"tool":"read","args":{"path":"forge.py","start_line":1,"end_line":10}}'
calls = forge.extract_tool_calls(json_text)
print(f"  Input: {json_text}")
print(f"  Parsed: {calls}")
assert calls[0]['tool'] == 'read'
assert calls[0]['args']['path'] == 'forge.py'

# Test 3: Tool parsing — Strategy 2 (Function calls)
print("\n[3] TOOL PARSING — FUNCTION CALLS")
func_text = 'call read("setup.py") or shell("ls -la", 30)'
calls = forge.extract_tool_calls(func_text)
print(f"  Input: {func_text}")
print(f"  Parsed: {calls}")
assert any(c['tool'] == 'read' for c in calls)
assert any(c['tool'] == 'shell' for c in calls)

# Test 4: Tool parsing — Strategy 3 (Markdown)
print("\n[4] TOOL PARSING — MARKDOWN CODE BLOCK")
md_text = 'The result:\n```json\n{"tool":"list","args":{}}\n```\nDone.'
calls = forge.extract_tool_calls(md_text)
print(f"  Input: {md_text[:50]}...")
print(f"  Parsed: {calls}")
assert calls[0]['tool'] == 'list'

# Test 5: Sloppy JSON Repair (Tiny Model specialty)
print("\n[5] SLOPPY JSON REPAIR")
sloppy_json = "{'tool': 'mkdir', 'args': {'path': 'src'}}"
calls = forge.extract_tool_calls(sloppy_json)
print(f"  Input: {sloppy_json}")
print(f"  Parsed: {calls}")
assert calls[0]['tool'] == 'mkdir'
assert calls[0]['args']['path'] == 'src'

# Test 6: Model profiles (Increased context)
print("\n[6] MODEL PROFILES")
models = ["qwen2.5:0.5b", "qwen2.5:3b", "qwen2.5:7b", "mistral:latest"]
for model in models:
    prof = forge.model_profile(model)
    print(f"  {model:20} -> {prof['label']:8} (max_context: {prof['max_context']})")
assert forge.model_profile("qwen2.5:0.5b")["max_context"] == 6

# Test 7: Few-shot prompt (Tiny Model)
print("\n[7] SYSTEM PROMPT (TINY MODEL)")
prompt = forge.build_system_prompt("/workspace", tiny=True)
print(f"  Contains 'EXAMPLES': {'EXAMPLES' in prompt}")
print(f"  Contains 'mkdir': {'mkdir' in prompt}")
print(f"  Length: {len(prompt)} chars")
assert "EXAMPLES" in prompt

print("\n" + "=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)

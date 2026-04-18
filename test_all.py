#!/usr/bin/env python3
"""Test all new Forge features"""
import forge
import json

print("=" * 60)
print("FORGE v0.4.0 TEST SUITE")
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

# Test 5: Context window with tokens
print("\n[5] CONTEXT WINDOW & TOKENS")
ctx = forge.ContextWindow("test system", max_msgs=5)
ctx.add("user", "hello")
ctx.add("assistant", "hi there")
ctx.add_tokens(100, 50)
print(f"  Messages: {len(ctx.messages)}")
print(f"  Tokens: {ctx.token_stats()}")
assert ctx.total_prompt_tokens == 100
assert ctx.total_completion_tokens == 50

# Test 6: Model profiles
print("\n[6] MODEL PROFILES")
models = ["qwen2.5:0.5b", "qwen2.5:3b", "qwen2.5:7b", "mistral:latest"]
for model in models:
    prof = forge.model_profile(model)
    print(f"  {model:20} -> {prof['label']:8} (max_context: {prof['max_context']})")

# Test 7: Few-shot prompt
print("\n[7] SYSTEM PROMPT (TINY MODEL)")
prompt = forge.build_system_prompt("/workspace", tiny=True)
print(f"  Contains 'EXAMPLES': {'EXAMPLES' in prompt}")
print(f"  Contains 'read': {'read' in prompt}")
print(f"  Length: {len(prompt)} chars")

print("\n" + "=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)

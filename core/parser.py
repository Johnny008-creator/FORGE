import json
import re

def repair_json(text):
    # Simple heuristic to fix single quotes and missing quotes on keys
    text = re.sub(r"'(\w+)':", r'"\1":', text)
    text = re.sub(r":\s*'([^']*)'", r': "\1"', text)
    return re.sub(r",\s*\}", "}", text)

def extract_tool_calls(text):
    calls = []
    # Strategy 1: Markdown blocks
    for m in re.finditer(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL):
        try: calls.append(json.loads(repair_json(m.group(1))))
        except: pass
    # Strategy 2: Raw JSON objects
    if not calls:
        for m in re.finditer(r'\{.*?"tool".*?\}', text, re.DOTALL):
            try: calls.append(json.loads(repair_json(m.group(0))))
            except: pass
    return [c for c in calls if "tool" in c]

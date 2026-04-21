# Configuration for TINY models (< 1.5B)
LABEL = "tiny"
MAX_CONTEXT = 4
NUM_PREDICT = 512
TEMPERATURE = 0.05

SYSTEM_HEADER = "You are Forge (tiny)."
RULES = "ONLY output JSON. No chatter. No preamble. One tool at a time."
EXAMPLES = """## EXAMPLES
User: list files
{"tool": "list", "args": {}}

User: read forge.py
{"tool": "read", "args": {"path": "forge.py"}}"""

REPAIR_JSON = True
FORCE_ONE_TOOL = True
DESC = "Optimized for < 1.5B models. Strict JSON & Few-shot."

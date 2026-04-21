# Configuration for SMALL models (1.5B - 4.0B)
LABEL = "small"
MAX_CONTEXT = 8
NUM_PREDICT = 1024
TEMPERATURE = 0.1

SYSTEM_HEADER = "You are Forge, a coding assistant."
RULES = "Use JSON for tools. State your plan briefly, then execute."
EXAMPLES = ""

REPAIR_JSON = True
FORCE_ONE_TOOL = False
DESC = "Optimized for 1.5B - 4B models. Balanced performance."

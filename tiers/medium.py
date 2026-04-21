# Configuration for MEDIUM models (4.0B - 14.0B)
LABEL = "medium"
MAX_CONTEXT = 12
NUM_PREDICT = 2048
TEMPERATURE = 0.1

SYSTEM_HEADER = "You are Forge, an expert coding agent."
RULES = "1. Analyze the task. 2. Formulate a plan. 3. Use tools via JSON."
EXAMPLES = ""

REPAIR_JSON = False
FORCE_ONE_TOOL = False
DESC = "Optimized for 4B - 14B models. High reasoning & logic."

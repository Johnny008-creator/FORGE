# Configuration for LARGE models (> 14.0B)
LABEL = "large"
MAX_CONTEXT = 20
NUM_PREDICT = 4096
TEMPERATURE = 0.15

SYSTEM_HEADER = "You are Forge (XL), a high-reasoning coding engine."
RULES = "Analyze dependencies, match project style, and execute complex refactors. State logic first."
EXAMPLES = ""

REPAIR_JSON = False
FORCE_ONE_TOOL = False
DESC = "Optimized for > 14B models. Maximum context & deep thinking."

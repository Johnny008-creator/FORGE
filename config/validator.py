import os
import requests
from ui.display import p_err, p_ok

def validate_startup(settings) -> bool:
    """Validates the environment before starting the agentic loop."""
    
    # 1. Validate Workdir
    if not os.path.isdir(settings.workdir):
        p_err(f"Invalid workdir: {settings.workdir}")
        return False
    
    # 2. Validate Ollama Connection
    try:
        r = requests.get(f"{settings.base_url}/api/tags", timeout=2)
        if r.status_code != 200:
            p_err(f"Ollama returned error: {r.status_code}")
            return False
    except Exception as e:
        p_err(f"Could not connect to Ollama at {settings.base_url}")
        return False
        
    p_ok("Environment validation successful.")
    return True

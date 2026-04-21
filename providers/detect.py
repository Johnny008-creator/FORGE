from providers.registry import PROVIDERS

def auto_detect_provider():
    """Tries to detect an available provider. Currently defaults to Ollama."""
    for name, provider in PROVIDERS.items():
        if provider.detect():
            return name, provider
    return None, None

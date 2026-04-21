from providers.ollama import OllamaProvider

PROVIDERS = {
    "ollama": OllamaProvider()
}

def get_provider(name: str):
    return PROVIDERS.get(name.lower())

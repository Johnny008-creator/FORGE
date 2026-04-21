import pytest
from config.settings import Settings
from core.context import ContextWindow
from providers.base import BaseProvider

@pytest.fixture
def mock_settings():
    return Settings(workdir="/tmp/test", exec_mode="auto", model_name="test-model")

@pytest.fixture
def sample_context():
    return ContextWindow("You are a test agent")

class MockProvider(BaseProvider):
    def detect(self): return "http://localhost:11434"
    def get_models(self): return [{"name": "test-model", "params_b": 7.0}]
    def stream_chat(self, messages, model, profile):
        return '{"tool": "list", "args": {}}', {"prompt": 10, "completion": 5}

@pytest.fixture
def mock_provider():
    return MockProvider()

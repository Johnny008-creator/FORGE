class TokenCounter:
    def __init__(self):
        self.prompt_tokens = 0
        self.completion_tokens = 0

    def add(self, prompt: int, completion: int):
        self.prompt_tokens += prompt
        self.completion_tokens += completion

    def get_stats(self) -> dict:
        return {
            "prompt": self.prompt_tokens,
            "completion": self.completion_tokens,
            "total": self.prompt_tokens + self.completion_tokens
        }

    def format_usage(self) -> str:
        s = self.get_stats()
        return f"{s['prompt']} in · {s['completion']} out (total: {s['total']})"

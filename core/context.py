class ContextWindow:
    def __init__(self, system):
        self.system = system
        self.messages = []
        self.total_in = 0
        self.total_out = 0

    def add(self, role, content):
        self.messages.append({"role": role, "content": content})

    def build(self):
        return [{"role": "system", "content": self.system}] + self.messages

    def trim(self, limit):
        if len(self.messages) > limit:
            self.messages = self.messages[-limit:]

# Hook API for Forge Plugins

class HookRegistry:
    def __init__(self):
        self._hooks = {
            "before_tool": [],
            "after_tool": [],
            "on_response": [],
            "on_error": []
        }

    def register(self, hook_name: str, fn):
        if hook_name in self._hooks:
            self._hooks[hook_name].append(fn)

    def fire(self, hook_name: str, **kwargs):
        if hook_name in self._hooks:
            for fn in self._hooks[hook_name]:
                try:
                    fn(**kwargs)
                except Exception as e:
                    print(f"Error in hook {hook_name}: {e}")

# Global instance for registry
registry = HookRegistry()

def on_hook(hook_name: str):
    """Decorator to register a function to a specific hook."""
    def decorator(fn):
        registry.register(hook_name, fn)
        return fn
    return decorator

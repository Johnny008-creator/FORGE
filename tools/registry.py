from tools.file import tool_read, tool_write, tool_patch, tool_delete, tool_mkdir
from tools.shell import tool_shell
from tools.search import tool_list, tool_search
from tools.ask import tool_ask_choice

TOOLS = {
    "read": (tool_read, "path [start] [end]"),
    "write": (tool_write, "path content"),
    "patch": (tool_patch, "path old new"),
    "list": (tool_list, "[path] [pattern]"),
    "search": (tool_search, "pattern [path]"),
    "shell": (tool_shell, "cmd"),
    "delete": (tool_delete, "path"),
    "mkdir": (tool_mkdir, "path"),
    "ask_choice": (tool_ask_choice, "question options"),
}

def register_tool(name, func, param_info):
    TOOLS[name] = (func, param_info)

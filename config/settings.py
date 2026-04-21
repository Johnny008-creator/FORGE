from dataclasses import dataclass
import os

@dataclass
class Settings:
    workdir: str = os.getcwd()
    exec_mode: str = "ask"
    base_url: str = "http://localhost:11434"
    model_name: str = ""
    debug: bool = False
    max_tool_output: int = 2000

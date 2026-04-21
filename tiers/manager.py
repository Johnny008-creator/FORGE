from tiers import tiny, small, medium, large

def get_tier_module(params_b):
    if params_b <= 1.5: return tiny
    if params_b <= 4.0: return small
    if params_b <= 14.0: return medium
    return large

def build_prompt(tier, workdir):
    tools_desc = """- read(path, [start], [end])
- write(path, content)
- patch(path, old, new)
- list([path], [pattern])
- search(pattern, [path])
- shell(cmd)
- delete(path)
- mkdir(path)
- ask_choice(question, options)"""

    p = f"{tier.SYSTEM_HEADER} Workdir: {workdir}\n\n"
    p += f"## RULES\n{tier.RULES}\n\n"
    if tier.EXAMPLES:
        p += f"{tier.EXAMPLES}\n\n"
    p += f"## AVAILABLE TOOLS\n{tools_desc}"
    return p

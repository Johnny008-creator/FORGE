from core.parser import extract_tool_calls
from tools import executor
from ui.display import p_warn, p_tool, p_tool_result

def agentic_loop(inp, ctx, model, provider, tier, counter):
    ctx.add("user", inp)
    last_calls = []
    
    for step in range(8):
        ctx.trim(tier.MAX_CONTEXT)
        # Using the provider instance instead of direct ollama call
        response, stats = provider.stream_chat(ctx.build(), model, tier.__dict__)
        
        counter.add(stats.get("prompt", 0), stats.get("completion", 0))
        ctx.total_in += stats.get("prompt", 0)
        ctx.total_out += stats.get("completion", 0)
        
        calls = extract_tool_calls(response)
        if tier.FORCE_ONE_TOOL and len(calls) > 1:
            calls = [calls[0]]
        
        if calls:
            if calls == last_calls:
                p_warn("Repetition detected - nudging...")
                ctx.add("assistant", response)
                ctx.add("user", f"[System: ERROR! You repeated '{calls[0]['tool']}'. Try something else.]")
                continue
            
            ctx.add("assistant", response)
            last_calls = calls
            for call in calls:
                name, args = call.get("tool"), call.get("args", {})
                p_tool(name, str(args)[:50], "run")
                
                if executor.should_confirm(name):
                    if not executor.ask_confirm(name, args):
                        ctx.add("user", f"[{name} cancelled by user]")
                        continue
                
                result = executor.run_tool(name, args)
                p_tool(name, str(args)[:50], "ok")
                p_tool_result(str(result)[:100].strip())
                ctx.add("user", f"[Result of {name}]\n{result}")
        else:
            ctx.add("assistant", response)
            if any(h in response.lower() for h in ["finish", "done", "success", "sorry"]):
                return
            ctx.add("user", "[System: No tool call found. Use JSON.]")

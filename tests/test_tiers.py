from tiers import manager, tiny, small, medium, large

def test_get_tier_module():
    assert manager.get_tier_module(0.5) == tiny
    assert manager.get_tier_module(1.5) == tiny
    assert manager.get_tier_module(3.0) == small
    assert manager.get_tier_module(8.0) == medium
    assert manager.get_tier_module(15.0) == large

def test_build_prompt():
    prompt = manager.build_prompt(tiny, "/tmp")
    assert "You are Forge (tiny)" in prompt
    assert "/tmp" in prompt
    assert "## RULES" in prompt

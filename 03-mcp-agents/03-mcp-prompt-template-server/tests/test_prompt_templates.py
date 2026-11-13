import pytest

from app.services.prompt_templates import (
    PromptInputError,
    TechnicalBriefRequest,
    render_technical_brief,
)


def test_renders_brief_with_defaults() -> None:
    prompt = render_technical_brief(TechnicalBriefRequest(topic="MCP servers"))

    assert "MCP servers" in prompt
    assert "Target audience: intermediate" in prompt
    assert "at least two concrete examples" in prompt


def test_can_disable_examples() -> None:
    prompt = render_technical_brief(
        TechnicalBriefRequest(
            topic="Vector databases",
            audience="expert",
            include_examples=False,
        )
    )

    assert "Target audience: expert" in prompt
    assert "Do not include examples" in prompt


@pytest.mark.parametrize("topic", ["", "AI", "x" * 121])
def test_rejects_invalid_topic(topic: str) -> None:
    with pytest.raises(PromptInputError, match="topic"):
        render_technical_brief(TechnicalBriefRequest(topic=topic))


def test_rejects_unknown_audience() -> None:
    with pytest.raises(PromptInputError, match="audience"):
        render_technical_brief(
            TechnicalBriefRequest(topic="MCP resources", audience="god-mode")
        )

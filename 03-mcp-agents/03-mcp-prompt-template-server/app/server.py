"""MCP server exposing a reusable technical brief prompt."""
from mcp.server.fastmcp import FastMCP

from app.services.prompt_templates import (
    TechnicalBriefRequest,
    render_technical_brief,
)

mcp = FastMCP("prompt-template-library")


@mcp.prompt()
def technical_brief(
    topic: str,
    audience: str = "intermediate",
    include_examples: bool = True,
) -> str:
    """Create a structured technical brief for a supplied topic."""
    return render_technical_brief(
        TechnicalBriefRequest(
            topic=topic,
            audience=audience,
            include_examples=include_examples,
        )
    )


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()

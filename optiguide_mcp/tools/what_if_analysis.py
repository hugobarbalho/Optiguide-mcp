from fastmcp import FastMCP


def setup_what_if_analysis(mcp: FastMCP):
    """Register the what-if-analysis tool with the MCP server."""
    @mcp.tool(
        "what-if-analysis",
        description="Given a question from the user, modify the formulation or data for a new scenario and resolve the problem.",
        annotations={
            "question": {"type": "string", "description": "User's what-if question"}
        }
    )
    async def what_if_analysis(question: str):
        # Placeholder implementation
        # TODO: Modify formulation/data based on question and resolve
        return {"analysis": "Not implemented"}

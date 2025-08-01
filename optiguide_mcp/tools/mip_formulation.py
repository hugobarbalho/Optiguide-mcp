from fastmcp import FastMCP, Context
from .util import send_prompt


def setup_mip_formulation(mcp: FastMCP):
    """Register the mip-formulation tool with the MCP server."""
    @mcp.tool(
        "mip-formulation",
        description="Given an optimization problem description, return the LaTeX formulation of a mixed integer programming problem.",
        annotations={
            "problem_description": {"type": "string", "description": "Description of the optimization problem"}
        }
    )
    async def mip_formulation(problem_description: str, ctx: Context):
        # Placeholder implementation
        # TODO: Generate LaTeX formulation from problem_description
        response = await send_prompt(ctx, f"Generate LaTeX formulation for the following optimization problem: {problem_description}")
        return {"latex": response}

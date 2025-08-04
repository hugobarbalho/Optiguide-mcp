from fastmcp import FastMCP, Context
from .util import send_prompt


def setup_what_if_analysis(mcp: FastMCP):
    """Register the what-if-analysis tool with the MCP server."""
    @mcp.tool(
        "what-if-analysis",
        description="Given a question from the user, modify the formulation or data for a new scenario and resolve the problem.",
        annotations={
            "original-problem-description": {"type": "string", "description": "Original problem description"},
            "original-latex-formulation": {"type": "string", "description": "Original LaTeX formulation"},
            "original-inputs": {"type": "object", "description": "Original inputs for the optimization problem"},
            "original-python-code": {"type": "string", "description": "Python code that needs to be modified to answer the question"},
            "question": {"type": "string", "description": "User's what-if question"}
        }
    )
    async def what_if_analysis(original_problem_description: str, original_latex_formulation: str, original_inputs: dict, original_python_code: str, question: str):
        # Placeholder implementation
        # TODO: Modify formulation/data based on question and resolve
        return {"analysis": "Not implemented yet"}

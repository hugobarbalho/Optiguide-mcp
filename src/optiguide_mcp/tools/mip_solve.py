from fastmcp import FastMCP, Context
from .util import send_prompt
import tempfile
import os
import re
from .util import run_as_main

code_gen_prompt = """
You are an expert in coding and debugging. Your task is to write python code using the pyomo solver.
Given a problem description, LaTeX formulation, and inputs, solve the optimization problem.
Return a python code snippet that can be used to solve the problem using Pyomo.
For formatting, use triple backticks with "python" to indicate the code block.
"""

code_example = """
import pyomo.environ as pyo

# Create a model
model = pyo.ConcreteModel()

# Define variables
model.x_A = pyo.Var(domain=pyo.NonNegativeIntegers)
model.x_B = pyo.Var(domain=pyo.NonNegativeIntegers)

# Parameters
Labor_A = 2
Labor_B = 1
Material_A = 3
Material_B = 2
Total_Labor = 100
Total_Material = 150
Profit_A = 40
Profit_B = 30

# Objective function
model.Profit = pyo.Objective(
    expr=Profit_A * model.x_A + Profit_B * model.x_B,
    sense=pyo.maximize
)

# Constraints
model.LaborConstraint = pyo.Constraint(
    expr=Labor_A * model.x_A + Labor_B * model.x_B <= Total_Labor
)
model.MaterialConstraint = pyo.Constraint(
    expr=Material_A * model.x_A + Material_B * model.x_B <= Total_Material
)

# Solve the model
solver = pyo.SolverFactory("appsi_highs")
result = solver.solve(model)

# Display the results
print(f"Optimal units of Product A (x_A): {pyo.value(model.x_A)}")
print(f"Optimal units of Product B (x_B): {pyo.value(model.x_B)}")
print(f"Maximum Profit: ${pyo.value(model.Profit)}")

    
"""


def setup_mip_solve(mcp: FastMCP):
    """Register the mip-solve tool with the MCP server."""
    @mcp.tool(
        "mip-solve",
        description="Given a problem description, LaTeX formulation, and inputs, solve the optimization problem.",
        annotations={
            "problem_description": {"type": "string", "description": "Description of the optimization problem"},
            "latex_formulation": {"type": "string", "description": "LaTeX formulation of the problem"},
            "inputs": {"type": "object", "description": "Inputs for the optimization problem"}
        }
    )
    async def mip_solve(ctx: Context, problem_description: str, latex_formulation: str, inputs: dict = ""):
        prompt = f"""
        {code_gen_prompt}

        *Problem Description:* 
        {problem_description}
        *LaTeX Formulation:*
        {latex_formulation}
        *Inputs:* 
        {inputs}
        *code example:*
        {code_example}
        """
        print("Generating LLM code ...")
        response = await send_prompt(ctx, prompt)
        #print("CODE RESPONSE:\n", response)
        code_response = response[0].content.text if isinstance(response, list) else response.content.text
        # Extract code from response (assume response is a string containing the code)
        # Extract python code that is between ```python ```
        python_code_str = re.findall(r"```python\n(.*?)```", code_response, re.DOTALL)[-1]
        #print("CODE EXTRACTED:\n", python_code_str)
        # Create a random temporary python file
        print("Saving code to temp file ...")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp_file:
            tmp_file.write(python_code_str)
            tmp_filename = tmp_file.name

        try:
            # Dynamically load the temp file as a module and run its solve() function
            print("Running code ...")
            output, error = await run_as_main(tmp_filename)

            status = "ok"
        except Exception as e:
            output = ""
            error = str(e)
            status = "error"
        finally:
            # Clean up the temporary file
            os.remove(tmp_filename)

        return {
            "python-code": python_code_str,
            "solution": output,
            "error": error,
            "status": status
        }

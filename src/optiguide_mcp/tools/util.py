from fastmcp import Context
from mcp.types import SamplingMessage, TextContent
from mcp.server.fastmcp.prompts import base

import io
from contextlib import redirect_stdout, redirect_stderr
import importlib.util
import sys

async def send_prompt(ctx:Context, prompt:str) -> str:
    try:
        result = await ctx.session.create_message(
        messages=[
                SamplingMessage(
                    role="user",
                    content=TextContent(type="text", text=prompt),
                )
            ],
            max_tokens=100,
        )

        if result.content.type == "text":
            return [base.Message(role="user", content=result.content.text)]
        return [base.Message(role="user", content=str(result.content))]
    except Exception as e:
        print(f"Failed to initialize the LLM model: {e}")
        raise RuntimeError(f"Could not initialize LLM: {e}") from e
    

async def run_as_main(script_path):
    # Load the module from the given script path
    captured_output = io.StringIO()
    captured_error = io.StringIO()
    
    # Redirect stdout within the context
    with redirect_stdout(captured_output), redirect_stderr(captured_error):
        spec = importlib.util.spec_from_file_location("__main__", script_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["__main__"] = module  # Set the module as __main__
        spec.loader.exec_module(module)  # Execute the module
    #return "Optimal units of Product 1 (x1): 560.00\nOptimal units of Product 2 (x2): 0.00\nOptimal overtime assembly labor hours (y): 50.00\nMaximum Profit: $3918.00\n",""
    return captured_output.getvalue(), captured_error.getvalue()
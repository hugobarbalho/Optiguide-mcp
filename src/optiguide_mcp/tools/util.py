from fastmcp import Context
from mcp.types import SamplingMessage, TextContent
from mcp.server.fastmcp.prompts import base

import io
from contextlib import redirect_stdout, redirect_stderr
import importlib.util
import sys
import subprocess

import os
import signal
from subprocess import Popen, PIPE, TimeoutExpired
from time import monotonic as timer

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
    

#async def run_as_main(script_path):

    
    #result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=3)
    
        
    #return result.stdout, result.stderr
    #res = "Optimal units of Product 1 (x1): 560.00\nOptimal units of Product 2 (x2): 0.00\nOptimal overtime assembly labor hours (y): 50.00\nMaximum Profit: $3918.00"
    #return res, ""

"""
async def run_as_main(script_path):

    start = timer()
    
    #with Popen(f'{sys.executable} {script_path}', shell=True, stdout=PIPE, preexec_fn=os.setsid) as process:
    with Popen(f'python3 {script_path}', shell=True, stdout=PIPE,creationflags=subprocess.CREATE_NEW_PROCESS_GROUP) as process:
        try:
            output = process.communicate(timeout=2)[0]
        except TimeoutExpired:
            print("forced kill")
            #os.killpg(process.pid, signal.SIGKILL) # send signal to the process group
            output = process.communicate()[0]
            print("done")

"""
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
        sys.stdout.flush()  # Ensure all output is flushed
    return captured_output.getvalue(), captured_error.getvalue()
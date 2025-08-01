from fastmcp import Context
from mcp.types import SamplingMessage, TextContent
from mcp.server.fastmcp.prompts import base

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
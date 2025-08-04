import argparse
import os
import warnings

import uvicorn
from fastmcp import FastMCP
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse
from starlette.middleware.cors import CORSMiddleware

# Create FastMCP server instance
mcp = FastMCP("OptiGuide MCP Server")

# Import tool setup functions
from optiguide_mcp.tools import setup_mip_formulation, setup_mip_solve, setup_what_if_analysis

# Setup tools
setup_mip_formulation(mcp)
setup_mip_solve(mcp)
setup_what_if_analysis(mcp)

# Custom HTTP routes
@mcp.custom_route("/", methods=["GET"])
async def root(request):
    return RedirectResponse(url="/docs")

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse({"status": "ok"})

@mcp.custom_route("/info", methods=["GET"])
async def mcp_info(request):
    tools_list = await mcp.get_tools()
    return JSONResponse({
        "status": "running",
        "protocol": "mcp",
        "server_name": "OptiGuide MCP Server",
        "tools_available": len(tools_list)
    })

@mcp.custom_route("/tools", methods=["GET"])
async def list_tools(request):
    tools = []
    tools_list = await mcp.get_tools()
    for tool_name, tool in tools_list.items():
        tools.append({
            "name": tool_name,
            "description": getattr(tool, "description", None) or "No description",
            "parameters": getattr(tool, "parameters", None) or {}
        })
    return JSONResponse({"tools": tools})

@mcp.custom_route("/docs", methods=["GET"])
async def docs(request):
    tools_list = await mcp.get_tools()
    docs_html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>OptiGuide MCP Server Documentation</title></head>
    <body>
        <h1>OptiGuide MCP Server Documentation</h1>
        <h2>Endpoints</h2>
        <ul>
            <li>GET /health</li>
            <li>GET /info</li>
            <li>GET /tools</li>
            <li>POST /mcp</li>
        </ul>
        <h2>Available Tools ({len(tools_list)})</h2>
        <ul>
    """
    for tool_name, tool in tools_list.items():
        docs_html += f"<li><strong>{tool_name}</strong>: {getattr(tool, 'description', 'No description')}</li>"
    docs_html += """
        </ul>
    </body>
    </html>
    """
    return HTMLResponse(content=docs_html)

def main():
    parser = argparse.ArgumentParser(description="OptiGuide MCP Server")
    parser.add_argument("--http", action="store_true", help="Run with HTTP transport")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Port (default: 8000)")
    parser.add_argument("--streamable-http", action="store_true", help="Run with streamable HTTP protocol")
    args = parser.parse_args()

    # Choose transport based on flags
    if args.http:
        port = int(os.environ.get("PORT", args.port))
        cors_middleware = CORSMiddleware(
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["*"],
            expose_headers=["mcp-session-id"],
            max_age=86400,
        )
        app = mcp.http_app(middleware=[cors_middleware])
        # Path redirect middleware
        class MCPPathRedirect:
            def __init__(self, app): self.app = app
            async def __call__(self, scope, receive, send):
                if scope.get('type') == 'http' and scope.get('path') == '/mcp':
                    scope['path'] = '/mcp/'
                    scope['raw_path'] = b'/mcp/'
                await self.app(scope, receive, send)
        app = MCPPathRedirect(app)
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
    elif args.streamable_http:
        # Run with streamable HTTP protocol
        mcp.run(transport="streamable-http", port=args.port)
    else:
        # Default stdio transport
        mcp.run(transport="stdio")

if __name__ == "__main__":
    main()

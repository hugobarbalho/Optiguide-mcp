# OptiGuide MCP Server

This is a Model Context Protocol (MCP) server providing optimization tools:

- mip_formulation: Given an optimization problem description, returns the LaTeX formulation of a mixed integer programming problem.
- mip_resolve: Given a problem description, LaTeX formulation, and inputs, solves the optimization problem.
- what_if_analysis: Given a question, modifies the formulation or data for a new scenario and resolves the problem.

## Installation

```powershell
python -m venv .venv; .\.venv\Scripts\activate; pip install -r requirements.txt
```

## Usage

```powershell
# Run with standard IO transport
python main.py

# Run with HTTP transport
python main.py --http --port 8000

# Run with streamable protocol
python main.py --streamable
```

## Tools

Visit `/tools` when the server is running to list available MCP tools.

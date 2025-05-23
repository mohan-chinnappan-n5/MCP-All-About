# demo_server.py
from mcp.server.fastmcp import FastMCP

# This is a simple example of how to use the FastMCP server
# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
# The tool adds two numbers
# The tool is a function that takes two integers and returns their sum
# The tool is registered with the server using the @mcp.tool() decorator

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"
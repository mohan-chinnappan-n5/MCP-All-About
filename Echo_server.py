from mcp.server.fastmcp import FastMCP
## pip install fastmcp


### This is a simple example of how to use the FastMCP server
# with the FastAPI framework.
# It creates a FastMCP server with a single resource, tool, and prompt.
# and the prompt creates a message to be processed.


mcp = FastMCP("Echo")


# The resource echoes a message, the tool echoes a message,
@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"

# The tool echoes a message, and the prompt creates a message to be processed.
@mcp.tool()
def echo_tool(message: str) -> str:
    """Echo a message as a tool"""
    return f"Tool echo: {message}"

# The prompt creates a message to be processed.
@mcp.prompt()
def echo_prompt(message: str) -> str:
    """Create an echo prompt"""
    return f"Please process this message: {message}"
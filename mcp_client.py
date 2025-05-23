import asyncio
import json
import requests
import argparse
import logging
import os
import re
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MCPClient:
    def __init__(self, model: str = "llama3"):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.ollama_endpoint = "http://localhost:11434/api/chat"
        self.model = model

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server
        
        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")
            
        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.client = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.client))
        
        await self.session.initialize()
        
        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        logger.info(f"Connected to server with tools: {[tool.name for tool in tools]}")
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def _call_ollama(self, messages: list, tools: list = None) -> dict:
        """Make a synchronous HTTP call to Ollama's chat API in an async context."""
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "max_tokens": 1000
        }
        if tools:
            payload["tools"] = tools

        # Run synchronous HTTP request in a thread pool
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: requests.post(self.ollama_endpoint, json=payload))
        
        if response.status_code != 200:
            raise ValueError(f"Ollama API error: {response.status_code} - {response.text}")
        
        return response.json()

    async def process_query(self, query: str) -> str:
        """Process a query using Ollama and available tools"""
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        response = await self.session.list_tools()
        available_tools = [{ 
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            }
        } for tool in response.tools]

        # Initial Ollama API call
        response = await self._call_ollama(messages, available_tools)

        # Process response and handle tool calls
        final_text = []

        # Ollama returns a single message in the response
        message = response.get("message", {})
        content = message.get("content", "")
        tool_calls = message.get("tool_calls", [])

        if content:
            final_text.append(content)

        for tool_call in tool_calls:
            tool_name = tool_call["function"]["name"]
            tool_args = tool_call["function"]["arguments"]
            
            # Execute tool call
            result = await self.session.call_tool(tool_name, tool_args)
            final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

            # Continue conversation with tool results
            if content:
                messages.append({
                    "role": "assistant",
                    "content": content
                })
            messages.append({
                "role": "tool",
                "content": result.content,
                "tool_call_id": tool_call.get("id", tool_name)
            })

            # Get next response from Ollama
            response = await self._call_ollama(messages)
            final_text.append(response["message"]["content"])

        return "\n".join(final_text)

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print(f"Using Ollama model: {self.model}")
        print("Type your queries or 'quit' to exit.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
                
                if query.lower() == 'quit':
                    break
                    
                response = await self.process_query(query)
                print("\n" + response)
                    
            except Exception as e:
                print(f"\nError: {str(e)}")
    
    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

def validate_server_script(value: str) -> str:
    """Validate that the server script is a .py or .js file."""
    if not (value.endswith('.py') or value.endswith('.js')):
        raise argparse.ArgumentTypeError("Server script must be a .py or .js file")
    if not os.path.isfile(value):
        raise argparse.ArgumentTypeError(f"Server script '{value}' does not exist")
    return value

async def main():
    parser = argparse.ArgumentParser(description="MCP Client for Ollama models")
    parser.add_argument(
        "server_script",
        type=validate_server_script,
        help="Path to the server script (.py or .js)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="llama3",
        help="Ollama model name (default: llama3)"
    )

    args = parser.parse_args()

    client = MCPClient(model=args.model)
    try:
        await client.connect_to_server(args.server_script)
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
# Model Context Protocol (MCP) - moves toward more integrated and context-aware AI

Large language models (LLMs) today are incredibly smart when we use them standalone, but they struggle once they need information beyond what’s in their frozen training data. So we need a way to let models go beyond their training data, making them more flexible and aware of the world around them.



For AI agents to be truly useful, they must access the **right context at the right time**
- files
- knowledge bases
- tools


Connecting an AI model (LLMs) to all these external sources has been a messy, ad-hoc affair.

- Developers had to write custom code or use specialized plugins for each data source or API. This made “wire together” integrations brittle and hard to scale.


Anthropic came up with Model Context Protocol (MCP) in November 2024 – an open standard designed to bridge AI assistants with the world of data and tools, to plug in many different sources of context. 
It is now becoming potential game-changer for building agentic AI systems.

MCP enables the shift toward more integrated, context-aware AI, its place in agentic workflows.

MCP addresses  “how to connect existing data sources” (file systems, databases, APIs, etc.) in AI workflows. 
This is required for production-ready AI agents.

Now, we have  over 1,000 community-built MCP servers (connectors) available.

MCP is open and model-agnostic, and it’s backed by a major AI player - Anthropic. Any developer or company can create an MCP integration without permission. Similar to USB, HTTP, or ODBC...


MCP lays out clear rules for how AI can find, connect to, and use external tools – whether it’s querying a database or running a command



## MCP details

- MCP uses [JSON RPC 2.0](#json-rpc2) - [Schema in ts](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/schema/2025-03-26/schema.ts) - [schema.json](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/schema/2025-03-26/schema.json)

- Components
    - Hosts - LLM apps that initiate connections (example Claude Desktop, your Agent app)
        - 
    - Clients  (eg. Claude Desktop)
        - invokes **tools**
        - queries for **resources**
        - interpolates **prompts**

    - Servers - Services that provide **context and capabilities**
        - Exposes tools via ```@mcp.tool()```
        - Exposes Resources
        - Exposes Prompts



## Simple  MCP server (add 2 integers)
```py
# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

```



## Dynamic Discovery

AI agents automatically detect **available MCP servers and their capabilities**, without hard-coded integrations. 

For example, if you spin up a new MCP server (like a Salesforce), agents can immediately recognize and use it via a standardized API, offering flexibility traditional approaches can't match.

The model/agent can now call the MCP tool actions as needed. Make sure to monitor logs to see that it’s calling the servers correctly. You’ll see requests hitting the MCP server and responses coming back.


<a name="json-rpc2"></a>

### JSON-RPC 2.0
    -  It is a lightweight **remote procedure call (RPC)** protocol encoded in JSON
    - It allows a client to call methods on a server (or vice versa) using JSON messages over **HTTP, WebSocket, or other transports**

    -  It’s simple, stateless, and transport-agnostic.
    - Requests and responses are JSON objects.
    - Method calls are named and can have parameters.
    - Supports notifications (calls without response).
    - Error handling is standardized.

For example, to call subtract method with parameters 42 and 23.
id (RequestId) is used to match the response.
```json
{
  "jsonrpc": "2.0",
  "method": "subtract",
  "params": [42, 23],
  "id": 1
}
```

Example response:
```json
{
  "jsonrpc": "2.0",
  "result": 19,
  "id": 1
}
```
Example Error:  (like the method does not exist).

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32601,
    "message": "Method not found"
  },
  "id": 1
}
```


## Integrating the agents with real-world business systems and data
- Initially, much attention went to **model capabilities and prompt techniques**, not to integration!


## Before MCP
- Retrieval-Augmented Generation (RAG) and Vector Databases

We supply context to LLMs via a retriever that searches a knowledge base (documents, embeddings) and injects the top results into the prompt to LLM.

- This addresses the knowledge cutoff or limited memory of models.
- However, RAG usually deals with static text snippets and doesn’t inherently let the **model perform actions** or queries beyond what’s indexed.

- MCP can work alongside RAG – for instance, an MCP server could interface with a vector database or search engine, allowing the model to issue search queries as a tool rather than implicitly relying on retrieval every prompt.

- MCP is a more general mechanism: where RAG gives passive context, MCP lets the model actively fetch or act on context through defined channels.

- In scenarios where up-to-date or interactive data is needed (say, querying a live database or posting an update), MCP extends beyond just retrieving text – it can trigger operations.


## MCP and agents
MCP is not itself an "agent framework"; rather, it acts as a standardized integration layer for agents.

MCP is all about the Action part – specifically, giving agents a standardized way to perform actions involving external data or tools.

It provides the plumbing that connects an AI agent to the outside world in a secure, structured manner. Without MCP (or something like it), every time an agent needs to do something in the world – whether fetching a file, querying a database, or invoking an API – developers would have to wire up a custom integration or use ad-hoc solutions. That’s like building a robot but having to custom-craft each finger to grasp different objects – tedious and not scalable.

MCP streamlines the integration of external functionalities, making agents more versatile, adaptable, and capable of performing sophisticated tasks across diverse contexts.


## Sample Use cases
Multi-Step, Cross-System Workflows Agentic systems often need to coordinate across platforms. Say an AI plans an event: it checks your calendar, books a venue, emails guests, arranges travel, and updates a budget sheet. Right now, this requires stitching APIs together manually. With MCP, all these actions happen through a single interface. The agent calls a series of MCP tools (one for each task), keeping shared context across them—no lost threads, no custom integrations.


### Challenges
- Previous agent-based frameworks have demonstrated that AI models can struggle with tool selection and execution. 
- MCP attempts to mitigate this by providing structured tool descriptions and specifications, but success still hinges on the quality of these descriptions and the AI’s ability to interpret them correctly.


## References

- [MCP](https://modelcontextprotocol.io/introduction)

- [What Is MCP, and Why Is Everyone – Suddenly!– Talking About It?](https://huggingface.co/blog/Kseniase/mcp)

- [Video:Building Agents with Model Context Protocol - Full Workshop with Mahesh Murag of Anthropic](https://www.youtube.com/watch?v=kQmXtrmQ5Zg)

- [Exposing Services with MCP](https://thefocus.ai/posts/exposing-services-with-mcp/)


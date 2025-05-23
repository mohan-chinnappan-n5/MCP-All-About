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

- MCP uses [JSON RPC 2.0](#json-rpc2)

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
id is used to match the response.
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




## References

- [MCP](https://modelcontextprotocol.io/introduction)

- [What Is MCP, and Why Is Everyone – Suddenly!– Talking About It?](https://huggingface.co/blog/Kseniase/mcp)

- [Video:Building Agents with Model Context Protocol - Full Workshop with Mahesh Murag of Anthropic](https://www.youtube.com/watch?v=kQmXtrmQ5Zg)


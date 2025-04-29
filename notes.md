# Types of MCP Transports

MCP transports are built with streaming in mind.  
- Streaming provides better support for long-running tasks 
- In general, 

Please check the [docs](https://modelcontextprotocol.io/specification) for the most up-to-date spec.

This document describes the **2025-03-26** version of the MCP spec.

## Stdio

Stdio is a transport method using **stdin** and **stdout** streams for communication.  
- The client starts the server as a subprocess & reads/writes to the streams.
- Results are sent as JSON-RPC messages.
- Messages are delimited by new lines.

Stderr is used by the server to output error logs, but can be ignored by the client.

## HTTP+SSE (deprecated in 2025-03-26)

Earlier versions of the MCP spec used SSE (Server-Sent Events) for transport.

### What is it
- SSE is a one-way communication method where the server sends updates to the client.
- The client calls an endpoint to setup a connection & session
- The server sets up a SSE connection & responds with an 'endpoint event'.
  - The endpoint event contains a URL for the client to call to make requests
  - The SSE connection is used to send messages back to the client.
  - If the connection is broken, there is no resumability 
    - Note: SSE supports resumability, but the old MCP spec does not

### Implications & Issues
- SSE requires a persistent connection. 
  - In the old spec, this connection lasts forever, until either side terminates
  - i.e. the connection in inherently stateful
  - a port is consumed by each client, when the clients may be inactive
  - lambdas or web functions cannot be supported because of this persistent connection requirement
- You MUST use sticky sessions (or session affinity) for load balancing, 
  - otherwise the server responding might not be the one with the connection
- Supporting SSE with a robust highly available system requires with proxies and queues and is non-trivial.
- Telemetry libraries won't work out of the box with SSE, because the same stream is used for all responses. 

For a full discussion of SSE & its issues, see [this discussion](https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/102).

## Streamable HTTP 

StreamableHTTP is a new transport method that combines HTTP and SSE. It aims to cover the limitations of SSE.

### What is it
- It is a hybrid transport method that lets the server to choose HTTP or SSE for responses
  - HTTP
    - Standard HTTP request/response model, for quick fire requests & response
    - Works for serverless architectures
  - SSE
    - The SSE connection is designed for longer running tasks
    - The SSE connection should last only for the duration of the request and not the entire session
      - Still works for serverless architecture - new connections are created for each request

For a practical explanation of the changes, see this [link](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/206). Else, take a look at the specs.


2) set-up a session

calls /health

then calls 
/sse on http1.1
params: transportType:sse, url:url -> qn: why is url required? (let's look at the spec)

--- connection is setup
After that, you keep sending events and include the session id

event: endpoint
data: /message?sessionId=03b65371-db8e-4c0b-b70b-f621b19f3527

event: message
data: {"jsonrpc":"2.0","id":0,"result":{"protocolVersion":"2024-11-05","capabilities":{"experimental":{},"prompts":{"listChanged":false},"resources":{"subscribe":false,"listChanged":false},"tools":{"listChanged":false}},"serverInfo":{"name":"sse","version":"1.6.0"}}}

The server is pushing data back afterwards
---

every new req from the client is a get req
every response from the server is through the SSE connection

open qns:
there is a 'id' field in the jsonprc response. what is it?
is that how ping works?


---
What happens if you make a req to a unkonwn session id?
- You get a session not found response with 404


--------------

https://learn.microsoft.com/en-us/connectors/custom-connectors/#2-secure-your-api


Microsoft Entra ID: The user is asked to sign in to Microsoft Entra ID (and if corporate policy enforces a user to have multifactor authentication, certificates, or a smart card, this also can be enforced here). This enforcement takes place between the user and Microsoft Entra ID, which is independent of the connector itself. Many services, especially those provided by Microsoft, use Microsoft Entra ID.

Basic authentication: The username and password are sent in the API request. These secrets are stored and encrypted in an internal token store that's accessible only by Microsoft Power Platform.

OAuth—The redirect URL of the connector is retrieved from the settings and sent back to the user to sign in to the service directly and grant consent. User credentials are not stored. Once sign-in is successful and the user has granted consent to access data on their behalf, an authorization code is sent back to Microsoft Power Platform. With that authorization code, an access token is then retrieved and stored internally. This access token is accessible only by Microsoft Power Platform.


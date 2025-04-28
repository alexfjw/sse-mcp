from fastmcp import FastMCP, Context
import asyncio

mcp = FastMCP(name="sse")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    # Initialize and run the server
    asyncio.run(mcp.run_sse_async(log_level="debug"))

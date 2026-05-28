# pip install fastmcp
from fastmcp import FastMCP
from datetime import datetime

# Initialize the server
mcp = FastMCP("SimpleServer")

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """A simple tool to add two numbers together."""
    return a + b

@mcp.tool()
def get_time() -> dict:
    """Returns the current time with timezone offset."""
    local_dt = datetime.now().astimezone()
    return {
        "current_time": local_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": local_dt.strftime("%Z"),
        "utc_offset": local_dt.strftime("%z")
    }

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8001)

# pip install fastmcp
import os
from datetime import datetime
from fastmcp import FastMCP

# Initialize the server
mcp = FastMCP("JournalServer")

@mcp.tool()
def travel_journal(action: str, content: str = "") -> str:
    """Save or read travel preferences and past trip notes. Action: 'save' or 'read'."""
    path = "travel_journal.txt"
    if action == "save":
        with open(path, "a") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d')}] {content}\n")
        return "Logged in your Travel Journal."
    else:
        if not os.path.exists(path):
            return "Journal is empty."
        with open(path, "r") as f:
            return f.read()

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8001)

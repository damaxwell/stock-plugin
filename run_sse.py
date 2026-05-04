import os
from server import mcp

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run("sse", port=port)
from mcp.server.fastmcp import FastMCP
import uvicorn

# UPDATED: Pass host and port here, in the constructor
mcp = FastMCP("knowledge-server", host="0.0.0.0", port=8000)

# --- Simulate Google Drive Tool ---
@mcp.tool()
def search_product_docs(query: str) -> str:
    """Searches internal product documentation (simulates Google Drive)."""
    mock_knowledge = {
        "pricing": "The Enterprise plan costs $50/user/month.",
        "api": "The API rate limit is 1000 req/min.",
        "deploy": "We use Kubernetes for deployment."
    }
    results = [v for k, v in mock_knowledge.items() if query.lower() in k.lower() or query.lower() in v.lower()]
    return "\n".join(results) if results else "No documentation found."

# --- Simulate Slack Tool ---
@mcp.tool()
def search_team_slack(keyword: str) -> str:
    """Searches team communication channels (simulates Slack)."""
    mock_chats = [
        "DevTeam: We fixed the memory leak in the Qdrant connector.",
        "Product: New UI launch is delayed to Friday.",
        "Ops: The API keys for GitHub are in the secure vault."
    ]
    results = [msg for msg in mock_chats if keyword.lower() in msg.lower()]
    return "\n".join(results) if results else "No relevant chats found."

if __name__ == "__main__":
    # UPDATED: Remove host/port arguments from here
    mcp.run(transport="sse")

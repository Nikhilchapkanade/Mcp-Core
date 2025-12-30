from langchain_core.tools import Tool

class MCPToolManager:
    def __init__(self):
        # The session will be assigned externally by server.py
        self.session = None

    async def get_langchain_tools(self) -> list[Tool]:
        if not self.session:
            print("⚠️ Warning: Attempted to get tools without active session.")
            return []

        # Get list of tools from the connected session
        mcp_tools = await self.session.list_tools()
        langchain_tools = []

        for tool in mcp_tools.tools:
            # Create the async wrapper for LangChain
            async def _invoke_mcp_tool(input_str: str, tool_name=tool.name):
                result = await self.session.call_tool(tool_name, arguments={"query": input_str})
                return result.content[0].text

            # Create the LangChain Tool object
            lc_tool = Tool(
                name=tool.name,
                func=None,
                coroutine=_invoke_mcp_tool,
                description=tool.description
            )
            langchain_tools.append(lc_tool)
            
        return langchain_tools
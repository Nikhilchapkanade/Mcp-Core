import os
from langchain_community.chat_models import ChatOllama
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain import hub
from mcp_client import MCPToolManager

class RAGAgent:
    def __init__(self):
        self.llm = ChatOllama(
            model="llama3.2", 
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=0
        )
        self.mcp_manager = MCPToolManager()
        self.executor = None

    async def initialize(self):
        # NOTE: Connection is now handled externally in server.py
        
        # 1. Get Tools from MCP
        tools = await self.mcp_manager.get_langchain_tools()
        
        # 2. Create Agent
        prompt = hub.pull("hwchase17/openai-tools-agent")
        agent = create_openai_tools_agent(self.llm, tools, prompt)
        self.executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

    async def process_query(self, query: str):
        if not self.executor:
            return "Agent initializing..."
        try:
            response = await self.executor.ainvoke({"input": query})
            return response["output"]
        except Exception as e:
            return f"Error processing query: {str(e)}"

# Global Instance
rag_system = RAGAgent()
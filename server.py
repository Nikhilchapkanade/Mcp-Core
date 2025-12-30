import asyncio
import os
import sys
import traceback  # <--- Added this to see the real error
from contextlib import asynccontextmanager
from fastapi import FastAPI
from mcp import ClientSession
from mcp.client.sse import sse_client
from agent import rag_system

MCP_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/sse")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting RAG Agent... (Attempting connection)", flush=True)
    
    while True:
        try:
            print(f"📡 Connecting to {MCP_URL}...", flush=True)
            
            async with sse_client(MCP_URL) as streams:
                async with ClientSession(streams[0], streams[1]) as session:
                    rag_system.mcp_manager.session = session
                    await session.initialize()
                    await rag_system.initialize()
                    
                    print("✅ MCP Connected Successfully!", flush=True)
                    yield 
                    print("🛑 Shutting down connection...", flush=True)
                    break 

        except (OSError, ConnectionError) as e:
            print(f"⚠️ Connection failed. Retrying in 5s... ({e})", flush=True)
            await asyncio.sleep(5)
        except Exception as e:
            # IGNORE CancelledError (happens when you stop the container)
            if isinstance(e, asyncio.CancelledError):
                break

            # PRINT THE REAL ERROR
            print("❌ DETAILED ERROR LOG:", flush=True)
            traceback.print_exc()  # <--- This prints the hidden error
            
            print("Retrying in 5s...", flush=True)
            await asyncio.sleep(5)

app = FastAPI(title="MCP RAG Agent", lifespan=lifespan)

@app.get("/query")
async def query_agent(q: str):
    response = await rag_system.process_query(q)
    return {"response": response}
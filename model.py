import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ariadne import ChatAriadne
from dotenv import load_dotenv
load_dotenv(override=True)

def get_model():
    model = {
        "openai": lambda: ChatOpenAI(model=os.getenv("LLM_MODEL"), api_key=os.getenv("LLM_API_KEY")),
        "anthropic": lambda: ChatAnthropic(model=os.getenv("LLM_MODEL"), api_key=os.getenv("LLM_API_KEY")),
        "ollama": lambda: ChatOllama(model=os.getenv("LLM_MODEL")),
        "google": lambda: ChatGoogleGenerativeAI(model=os.getenv("LLM_MODEL"), google_api_key=os.getenv("LLM_API_KEY")),
        "ariadne": lambda: ChatAriadne(model=os.getenv("LLM_MODEL"), api_key=os.getenv("LLM_API_KEY"), base_url=os.getenv("LLM_BASE_URL"), provider=os.getenv("LLM_PROVIDER_NAME"))
    }[os.getenv("LLM_PROVIDER")]()
    return model

import asyncio
import streamlit as st
from langchain_mcp_adapters.client import MultiServerMCPClient

@st.cache_resource
def get_mcp_model():
    model = get_model()

    # Configuration for your ALREADY RUNNING MCP server
    server_config = {
        "my_remote_server": {
            "url": "http://localhost:8000/mcp",
            "transport": "http"
        }
    }
    
    async def fetch_tools():
        client = MultiServerMCPClient(server_config)
        return await client.get_tools()
    
    # Pull tools from the server and bind them to the LLM
    tools = asyncio.run(fetch_tools())
    tool_map = {t.name: t for t in tools}
    return model.bind_tools(tools), tool_map

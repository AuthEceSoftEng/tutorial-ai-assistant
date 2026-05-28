"""
Phase 5: The Resilient Parallel Agent
-------------------------------------
This script implements the final, most advanced step of our hands-on workshop:
A highly capable, resilient AI Agent running inside Chainlit.

Key features in this phase:
1. **Parallel Tool Execution**: Uses `asyncio.gather()` to execute multiple tool calls 
   requested by the LLM simultaneously (speed offense).
2. **Defensive Error Resilience**: Wraps tool executions in try-except blocks, 
   returning tool exceptions gracefully as `ToolMessage` feedback so the LLM can 
   self-correct instead of crashing.
3. **Collapsible Run Logs**: Uses Chainlit's native `cl.Step` to render active tool 
   execution steps directly in the chat bubbles.
4. **Dynamic Setup Checks**: Automatically verifies if the advanced MCP server 
   is running before starting the chat.

To run this step:
  1. Start the MCP server: python mcpserver_advanced.py
  2. Launch the agent:     chainlit run main4_agent_chainlit.py
"""

import asyncio
import chainlit as cl
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from model import get_model

# central model loader
aimodel = get_model()

# Automatically launch mcpserver.py in the background on Port 8001
import subprocess, time
print("Launching Simple Travel Buddy MCP Server on Port 8001 in the background...", flush=True)
subprocess.run(["pkill", "-f", "mcpserver.py"], capture_output=True)
time.sleep(1)
subprocess.Popen(["python3", "mcpserver.py"])
time.sleep(2) # Give it a moment to bind and listen


# Configuration for our running simple MCP server
MCP_SERVER_CONFIG = {
    "my_mcp_server": {
        "url": "http://localhost:8001/mcp",
        "transport": "http"
    }
}

@cl.on_chat_start
async def on_chat_start():
    """
    Called when the chat session starts. 
    Connects to the running MCP server, extracts available tools, and binds them to the LLM.
    """
    try:
        # 1. Connect to MCP server and fetch tool schemas
        mcp_client = MultiServerMCPClient(MCP_SERVER_CONFIG)
        tools = await mcp_client.get_tools()
        tool_map = {t.name: t for t in tools}
        
        # 2. Bind the tools to our standard LangChain model
        bound_model = aimodel.bind_tools(tools)
        
        # Save model and tool reference in the session cache
        cl.user_session.set("bound_model", bound_model)
        cl.user_session.set("tool_map", tool_map)
        
        # Initialize conversation state
        try:
            with open("system_prompt.txt", "r") as f:
                system_prompt = f.read().strip()
        except FileNotFoundError:
            system_prompt = "You are a helpful and professional AI assistant with system and travel tools."
            
        cl.user_session.set("messages", [SystemMessage(content=system_prompt)])
        
    except Exception as e:
        # Send error notification only if connection fails so the user knows they need to check port 8001
        await cl.Message(
            content=(
                "**Failed to connect to the MCP Server!**\n\n"
                "Please make sure the simple MCP server is running first:\n"
                "```bash\n"
                "python mcpserver.py\n"
                "```\n"
                f"Error details: `{str(e)}`"
            )
        ).send()


async def run_single_tool(tool_call, tool_map) -> ToolMessage:
    """
    Executes a single tool call asynchronously inside a nested Chainlit Step.
    Features defensive try-except blocks to feed failures back to the LLM for self-correction.
    """
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]
    tool_id = tool_call["id"]
    
    # Render a collapsible execution block inside Chainlit
    async with cl.Step(name=f"Tool: {tool_name}") as step:
        step.input = tool_args
        
        # Defensive check for tool name hallucinations
        if tool_name not in tool_map:
            error_msg = f"Error: Tool '{tool_name}' not found on server. Available tools: {list(tool_map.keys())}"
            step.output = error_msg
            return ToolMessage(content=error_msg, tool_call_id=tool_id)
            
        try:
            # Execute the tool call asynchronously
            tool_result = await tool_map[tool_name].ainvoke(tool_args)
            step.output = str(tool_result)
            return ToolMessage(content=str(tool_result), tool_call_id=tool_id)
            
        except Exception as e:
            # Capture traceback/exception and format it as ToolMessage context
            error_msg = f"Exception raised: {str(e)}"
            step.output = error_msg
            return ToolMessage(content=error_msg, tool_call_id=tool_id)


@cl.on_message
async def on_message(message: cl.Message):
    """
    Main agentic messaging loop. Intercepts tool calls, executes them in parallel, 
    feeds results back to the LLM, and streams final responses.
    """
    bound_model = cl.user_session.get("bound_model")
    tool_map = cl.user_session.get("tool_map")
    
    if not bound_model or not tool_map:
        await cl.Message(content="Please wait until the MCP connection is established.").send()
        return
        
    messages = cl.user_session.get("messages")
    messages.append(HumanMessage(content=message.content))
    
    # 1. Create an empty message bubble for the assistant's reply
    assistant_msg = cl.Message(content="")
    await assistant_msg.send()
    
    try:
        # 2. Initial LLM invocation to check if tool calls are requested
        response = await bound_model.ainvoke(messages)
        
        # 3. Keep executing tools in a loop as long as the LLM requests them
        while response.tool_calls:
            # Append the LLM's raw tool request intent to history
            messages.append(response)
            
            # Speed Offense: Build concurrent tasks to execute all tool calls in parallel!
            tasks = [run_single_tool(tc, tool_map) for tc in response.tool_calls]
            tool_results = await asyncio.gather(*tasks)
            
            # Append all tool execution results back to history
            for result_msg in tool_results:
                messages.append(result_msg)
                
            # Re-invoke the LLM with the new grounded context from tool runs
            response = await bound_model.ainvoke(messages)
            
        full_response = response.content
        if isinstance(full_response, list):
            full_response = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in full_response])
        else:
            full_response = str(full_response)
            
        # Stream response to the screen block-by-block with a natural reading pace
        words = full_response.split(" ")
        for idx, word in enumerate(words):
            space = " " if idx > 0 else ""
            await assistant_msg.stream_token(space + word)
            await asyncio.sleep(0.01) # Natural pacing
            
        # Save final verbal assistant response to conversation history
        messages.append(response)
        
    except Exception as e:
        error_info = str(e)
        if "429" in error_info or "quota" in error_info.lower():
            err_msg = "**API Quota Exceeded (429 Rate Limit)**: Please wait a moment before sending another prompt."
        else:
            err_msg = f"**Agent Error**: {error_info}"
        
        await assistant_msg.stream_token(err_msg)
        messages.append(AIMessage(content=err_msg))
        
    # 4. Finalize the message bubbles and save context back to session
    await assistant_msg.update()
    cl.user_session.set("messages", messages)

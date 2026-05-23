import streamlit as st
import asyncio
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from model import get_mcp_model

# --- 1. MCP & MODEL SETUP ---
aimodel, tool_map = get_mcp_model()
st.title("Simple AI Assistant (" + (str(aimodel.bound.model) if aimodel else "No Model Found") + ")")

# --- 2. SESSION STATE ---
if "messages" not in st.session_state:
    with open("system_prompt.txt", "r") as infile:
        system_prompt_text = infile.read().strip()
    st.session_state.messages = [SystemMessage(content=system_prompt_text)]

# --- 3. DISPLAY CHAT HISTORY ---
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    
    elif isinstance(msg, AIMessage):
        # We only show the bubble if there is text or tool calls
        if msg.content or msg.tool_calls:
            with st.chat_message("assistant"):
                if msg.content:
                    st.write(msg.content)
                if msg.tool_calls:
                    for tc in msg.tool_calls:
                        st.status(f"Used tool: {tc['name']}", state="complete")

    elif isinstance(msg, ToolMessage):
        # Tool results are usually hidden in a collapse for a clean UI
        with st.expander(f"Tool Data ({msg.tool_call_id})"):
            st.code(msg.content)

# --- 4. CHAT INPUT & AGENTIC LOOP ---
if prompt := st.chat_input("Ask me something..."):
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        # 1. We still use .invoke() for the initial check to see if tools are needed
        # (Tool calls cannot be easily streamed in a simple tutorial)
        response = aimodel.invoke(st.session_state.messages)
        
        # 2. Execute tools if the AI requested them
        while response.tool_calls:
            st.session_state.messages.append(response)
            for tc in response.tool_calls:
                with st.status(f"Running {tc['name']}...", expanded=False) as status:
                    tool_result = asyncio.run(tool_map[tc["name"]].ainvoke(tc["args"]))
                    st.session_state.messages.append(
                        ToolMessage(content=str(tool_result), tool_call_id=tc["id"])
                    )
                    status.update(label=f"Completed {tc['name']}", state="complete")

            # After tools run, we check again if the AI needs more tools
            response = aimodel.invoke(st.session_state.messages)

        # 3. NOW WE STREAM: Once all tools are done, stream the final verbal response
        response_placeholder = st.empty()
        full_response = ""
        
        # We stream based on the latest state of messages (including tool results)
        for chunk in aimodel.stream(st.session_state.messages):
            if isinstance(chunk.content, list):
                for part in chunk.content:
                    if isinstance(part, dict) and "text" in part:
                        full_response += part["text"]
                    elif isinstance(part, str):
                        full_response += part
            else:
                full_response += chunk.content
            response_placeholder.markdown(full_response + "|")
        
        response_placeholder.markdown(full_response)
        
        # Store the final text answer in history
        st.session_state.messages.append(AIMessage(content=full_response))


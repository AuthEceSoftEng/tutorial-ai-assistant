import streamlit as st
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from model import get_model

st.title("Simple AI Assistant")

# --- 1. MCP & MODEL SETUP ---
aimodel = get_model()

# --- 2. SESSION STATE ---
if "messages" not in st.session_state:
    with open("system_prompt.txt", "r") as infile:
        system_prompt_text = infile.read().strip()
    st.session_state.messages = [SystemMessage(content=system_prompt_text)]

# 2. Display Chat History (Skips the system prompt)
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    elif isinstance(msg, AIMessage):
        st.chat_message("assistant").write(msg.content)

# 3. Chat Input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)

    # 4. Stream the Response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Using the same .stream() logic you already have
        for chunk in aimodel.stream(st.session_state.messages):
            full_response += chunk.content
            response_placeholder.markdown(full_response + "|")
        
        response_placeholder.markdown(full_response)
    
    st.session_state.messages.append(AIMessage(content=full_response))
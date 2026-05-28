"""
Phase 3: Moving to a Web UI with Chainlit
-----------------------------------------
This script transitions our CLI chatbot into a browser-based conversational interface 
using Chainlit. 

In this phase:
1. We introduce Chainlit callbacks (`on_chat_start` and `on_message`).
2. We manage chat history persistent at the user-session level (`cl.user_session`).
3. We implement asynchronous token-by-token streaming directly into chat bubbles.

To run this step:
  chainlit run main3_chainlit.py
"""

import chainlit as cl
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from model import get_model

# central model loader
aimodel = get_model()

@cl.on_chat_start
async def on_chat_start():
    """
    Triggered when a user opens the chat in their browser.
    We set up the initial system instructions and establish session-level history.
    """
    # Load system prompt
    try:
        with open("system_prompt.txt", "r") as infile:
            system_prompt_text = infile.read().strip()
    except FileNotFoundError:
        system_prompt_text = "You are a helpful and professional AI assistant."
    
    # Store message history inside Chainlit's session storage
    cl.user_session.set("messages", [SystemMessage(content=system_prompt_text)])

@cl.on_message
async def on_message(message: cl.Message):
    """
    Triggered every time a user types a message and hits enter.
    """
    # 1. Retrieve the conversation history from the user session
    messages = cl.user_session.get("messages")
    
    # 2. Append the new user message
    messages.append(HumanMessage(content=message.content))
    
    # 3. Create an empty Chainlit message bubble for the assistant's reply
    assistant_msg = cl.Message(content="")
    await assistant_msg.send()
    
    # 4. Stream the LLM response asynchronously
    full_response = ""
    try:
        # .astream() is LangChain's native async token-by-token generator
        async for chunk in aimodel.astream(messages):
            content = chunk.content
            if isinstance(content, str):
                full_response += content
                # Stream tokens to the screen
                await assistant_msg.stream_token(content)
    except Exception as e:
        error_info = str(e)
        if "429" in error_info or "quota" in error_info.lower():
            err_msg = "\n\n**API Quota Exceeded (429 Rate Limit)**: Please wait a moment before sending another prompt."
        else:
            err_msg = f"\n\n**Connection/API Error**: {error_info}"
        full_response += err_msg
        await assistant_msg.stream_token(err_msg)
            
    # 5. Finalize the message and commit the complete assistant response to memory
    await assistant_msg.update()
    messages.append(AIMessage(content=full_response))
    
    # 6. Save the updated conversation history back to the session
    cl.user_session.set("messages", messages)

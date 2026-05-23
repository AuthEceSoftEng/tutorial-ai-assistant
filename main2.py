from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from model import get_model

aimodel = get_model()
with open("system_prompt.txt", "r") as infile:
    system_prompt_text = infile.read().strip()
system_prompt = SystemMessage(content=system_prompt_text)

print("AI Assistant is ready! (Type 'exit' to stop)")

messages = [system_prompt]

while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    
    messages.append(HumanMessage(content=user_input))
    
    # Get response
    print("AI: ", end="", flush=True) # Print prefix without a newline
    full_response = "" # Use .stream() instead of .invoke()
    for chunk in aimodel.stream(messages):  # @UndefinedVariable
        content = chunk.content
        print(content, end="", flush=True) # Print tokens as they arrive
        full_response += content
    print() # Add a newline at the end
    
    # Update history for context
    messages.append(AIMessage(content=full_response))

from langchain_core.messages import SystemMessage, HumanMessage
from model import get_model

aimodel = get_model()
system_prompt = SystemMessage(content="You are a helpful AI assistant. Your tone is professional yet friendly.")

print("AI Assistant is ready! (Type 'exit' to stop)")

messages = [system_prompt]

while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    
    messages.append(HumanMessage(content=user_input))
    
    # Get response
    response = aimodel.invoke(messages)  # @UndefinedVariable
    
    print(f"\nAI: {response.content}")
    
    # Update history for context
    messages.append(response)

import os
from dotenv import load_dotenv
load_dotenv(override=True)

def get_model():
    prov = os.getenv("LLM_PROVIDER", "google").lower()
    model_name = os.getenv("LLM_MODEL", "gemini-2.5-flash")
    api_key = os.getenv("LLM_API_KEY")
    
    # Defensive check: if the API key is not set or is placeholder, use a dummy string
    # to prevent a ValueError crash on startup instantiation
    if not api_key or api_key == "PASTE_YOUR_API_KEY_HERE":
        api_key = "dummy_key_to_prevent_startup_crash"
        
    if prov == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key, max_retries=0)
    elif prov == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=model_name, api_key=api_key)
    elif prov == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model=model_name, api_key=api_key)
    elif prov == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(model=model_name)
    elif prov == "ariadne":
        from langchain_ariadne import ChatAriadne
        return ChatAriadne(
            model=model_name, 
            api_key=api_key, 
            base_url=os.getenv("LLM_BASE_URL"), 
            provider=os.getenv("LLM_PROVIDER_NAME")
        )
    else:
        raise ValueError(f"Unknown provider: {prov}")

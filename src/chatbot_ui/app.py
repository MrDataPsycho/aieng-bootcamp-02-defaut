import streamlit as st
import httpx

from core.config import config

## Lets create a sidebar with a dropdown for the model list and providers
with st.sidebar:
    st.title("Settings")

    #Dropdown for provider
    provider = st.selectbox("Provider", ["OpenAI", "Groq", "Google"])

    if provider == "OpenAI":
        model_name = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o"])
    else:
        st.warning(f"{provider} is not available yet")
        model_name = None

    # Save provider and model to session state
    st.session_state.provider = provider
    st.session_state.model_name = model_name


def run_llm(messages):
    """Send chat request to backend API using httpx."""
    payload = {
        "provider": st.session_state.provider,
        "model_name": st.session_state.model_name,
        "messages": messages
    }

    try:
        with httpx.Client() as client:
            response = client.post(
                f"{config.BACKEND_API_URL}/chat",
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()["message"]
    except httpx.HTTPError as e:
        st.error(f"Error communicating with backend API: {str(e)}")
        return "Sorry, I encountered an error. Please try again."


if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Hello! How can I assist you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        answer = run_llm(st.session_state.messages)
        st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
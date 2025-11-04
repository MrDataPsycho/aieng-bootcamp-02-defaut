import streamlit as st
import requests
import logging
logging.getLogger("watchdog").setLevel(logging.INFO)

from core.config import config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

## Lets create a sidebar with a dropdown for the model list and providers
with st.sidebar:
    st.title("Settings")

    #Dropdown for model
    provider = st.selectbox("Provider", ["OpenAI", "Groq", "Google"])
    if provider == "OpenAI":
        model_name = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o"])
    elif provider == "Groq":
        model_name = st.selectbox("Model", ["llama-3.3-70b-versatile"])
    else:
        model_name = st.selectbox("Model", ["gemini-2.0-flash"])

    # Save provider and model to session state
    st.session_state.provider = provider
    st.session_state.model_name = model_name


def api_call(method, url, **kwargs):

    def _show_error_popup(message):
        """Show error message as a popup in the top-right corner."""
        st.session_state["error_popup"] = {
            "visible": True,
            "message": message,
        }

    try:
        response = getattr(requests, method)(url, **kwargs)

        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            logger.error("Invalid response format from server")
            response_data = {"message": "Invalid response format from server"}

        if response.ok:
            return True, response_data

        logger.error(f"API call failed: {response_data}")
        return False, response_data

    except requests.exceptions.ConnectionError as ce:
        logger.error(f"Connection error: {ce}")
        _show_error_popup("Connection error. Please check your network connection.")
        return False, {"message": "Connection error"}
    except requests.exceptions.Timeout as te:
        logger.error(f"Request timeout: {te}")
        _show_error_popup("The request timed out. Please try again later.")
        return False, {"message": "Request timeout"}
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        _show_error_popup(f"An unexpected error occurred: {str(e)}")
        return False, {"message": str(e)}


if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Hello! How can I assist you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    logger.info(f"User prompt: {prompt}")
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        output = api_call("post", f"{config.API_URL}/chat", json={"provider": st.session_state.provider, "model_name": st.session_state.model_name, "messages": st.session_state.messages})
        response_data = output[1]
        answer = response_data["message"]
        logger.info(f"Assistant response: {answer}")
        st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
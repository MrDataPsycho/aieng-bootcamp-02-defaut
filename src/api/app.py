from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from openai import OpenAI


from src.api.core.config import config

import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def run_llm(provider, model_name, messages, max_tokens=500):
    if provider.lower() == "openai":
        client = OpenAI(api_key=config.OPENAI_API_KEY)
    else:
        raise ValueError(f"Provider '{provider}' is not available yet")

    return client.chat.completions.create(
        model=model_name,
        messages=messages,
        max_tokens=max_tokens
    ).choices[0].message.content


class ChatRequest(BaseModel):
    provider: str
    model_name: str
    messages: list[dict]

class ChatResponse(BaseModel):
    message: str


app = FastAPI()

@app.post("/chat")
def chat(
    payload: ChatRequest
) -> ChatResponse:
    """
    CURL Body Example:
    {
        "provider": "openai",
        "model_name": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "Hello, how are you?"}]
    }
    """
    # Validate provider
    if payload.provider.lower() in ["groq", "google"]:
        raise HTTPException(
            status_code=400,
            detail=f"Provider '{payload.provider}' is not available yet"
        )

    result = run_llm(payload.provider, payload.model_name, payload.messages)

    return ChatResponse(message=result)
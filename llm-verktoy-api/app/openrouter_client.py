import os
import httpx

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
}
# Funksjon som caller openrouter
async def call_openrouter(messages, model="openai/gpt-4o-mini"):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            OPENROUTER_URL,
            headers=HEADERS,
            json={"model": model, "messages": messages},
            timeout=60.0,
        )
        response.raise_for_status()
        return response.json()
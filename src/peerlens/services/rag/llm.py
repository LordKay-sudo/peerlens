import httpx

from peerlens.config import Settings, get_settings
from peerlens.core.exceptions import RAGError


class OpenAIClient:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        if not self.settings.openai_api_key:
            raise RAGError(
                "OPENAI_API_KEY is not set. Add it to .env to use RAG Q&A."
            )

    async def embed(self, texts: list[str]) -> list[list[float]]:
        url = f"{self.settings.openai_base_url.rstrip('/')}/embeddings"
        headers = {
            "Authorization": f"Bearer {self.settings.openai_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.settings.embedding_model,
            "input": texts,
        }

        async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds) as client:
            response = await client.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            raise RAGError(f"Embedding request failed ({response.status_code}): {response.text}")

        data = response.json()["data"]
        return [item["embedding"] for item in sorted(data, key=lambda row: row["index"])]

    async def complete(self, system_prompt: str, user_prompt: str) -> str:
        url = f"{self.settings.openai_base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.settings.openai_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.settings.llm_model,
            "temperature": 0.2,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }

        async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds) as client:
            response = await client.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            raise RAGError(f"Chat completion failed ({response.status_code}): {response.text}")

        return response.json()["choices"][0]["message"]["content"].strip()

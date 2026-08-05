from openai import OpenAI
import os


class EmbeddingClient:

    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def embed(self, text: str) -> list[float]:

        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        return response.data[0].embedding

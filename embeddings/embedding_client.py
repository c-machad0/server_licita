import os

from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()


class EmbeddingClient:

    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def embed(self, text: str) -> list[float]:
        """
        Gera um embedding para o texto informado usando a API da OpenAI.

        Args:
            text: Texto que será convertido em embedding.

        Returns:
            list[float]: Vetor numérico correspondente ao texto.
        """

        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        return response.data[0].embedding

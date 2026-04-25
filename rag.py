import os
from openai import OpenAI
import faiss
import numpy as np
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class RAG:
    def __init__(self):
        self.chunks = []
        self.index = None

    def split_text(self, text):
        return [c.strip() for c in text.split("\n") if c.strip()]

    def build_index(self, text):
        self.chunks = self.split_text(text)

        embeddings = []
        for chunk in self.chunks:
            emb = client.embeddings.create(
                model="text-embedding-3-small",
                input=chunk
            )
            embeddings.append(emb.data[0].embedding)

        dimension = len(embeddings[0])
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings))

    def query(self, question):
        if self.index is None:
            return "No document uploaded yet."

        q_emb = client.embeddings.create(
            model="text-embedding-3-small",
            input=question
        ).data[0].embedding

        D, I = self.index.search(np.array([q_emb]), k=3)

        context = "\n".join([self.chunks[i] for i in I[0]])

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """Answer ONLY using the provided context.
If answer is not in context, say: I don't know."""
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {question}"
                }
            ]
        )

        return response.choices[0].message.content


rag = RAG()
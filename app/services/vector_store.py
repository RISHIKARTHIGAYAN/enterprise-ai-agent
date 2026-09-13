from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import (
    CHROMA_COLLECTION,
    CHROMA_DIRECTORY,
    EMBEDDING_MODEL,
)


class VectorStore:

    def __init__(self):

        Path(CHROMA_DIRECTORY).mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = chromadb.PersistentClient(
            path=str(CHROMA_DIRECTORY)
        )

        self.collection = self.client.get_or_create_collection(
            name=CHROMA_COLLECTION
        )

        self.embedding_model = SentenceTransformer(
            EMBEDDING_MODEL
        )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=120,
        )

    def ingest(self, documents):

        ids = []
        texts = []
        metadatas = []
        embeddings = []

        for document in documents:

            chunks = self.splitter.split_text(
                document["text"]
            )

            for index, chunk in enumerate(chunks):

                chunk_id = (
                    f'{document["source"]}_{index}'
                )

                ids.append(chunk_id)
                texts.append(chunk)

                metadatas.append(
                    {
                        "source": document["source"],
                        "chunk": index,
                    }
                )

                embeddings.append(
                    self.embedding_model.encode(
                        chunk
                    ).tolist()
                )

        if not ids:
            return 0

        self.collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings,
        )

        return len(ids)

    def search(
        self,
        query,
        top_k=5,
    ):

        query_embedding = (
            self.embedding_model.encode(
                query
            ).tolist()
        )

        results = self.collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=top_k,
        )

        documents = results.get(
            "documents",
            [[]],
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]],
        )[0]

        distances = results.get(
            "distances",
            [[]],
        )[0]

        output = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):

            output.append(
                {
                    "text": document,
                    "source": metadata.get(
                        "source",
                        "unknown",
                    ),
                    "distance": float(
                        distance
                    ),
                }
            )

        return output
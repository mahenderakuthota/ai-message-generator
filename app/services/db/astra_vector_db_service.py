from langchain_astradb import AstraDBVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
import csv

from app.services.db.vector_store_service import VectorStoreService


class AstraVectorStoreService(VectorStoreService):

    def get_vector_store(self) -> object:
        return self.vectorstore

    def __init__(self, **kwargs):
        load_dotenv()
        self.astra_db_token = os.getenv("ASTRA_DB_TOKEN")
        self.astra_db_id = os.getenv("ASTRA_DB_ID")
        self.astra_db_region = os.getenv("ASTRA_DB_REGION")
        print(f"ASTRA_DB_TOKEN: {self.astra_db_token}, ASTRA_DB_ID: {self.astra_db_id}, ASTRA_DB_REGION: {self.astra_db_region}")
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = AstraDBVectorStore(
            embedding=embeddings,
            collection_name="flirt_messages",
            api_endpoint=f"https://{self.astra_db_id}-{self.astra_db_region}.apps.astra.datastax.com",
            token=self.astra_db_token
        )
        print("vector store initialized")
        print(self.vectorstore.as_retriever())

    def load_data(self,csv_file):
        flirt_data = []
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                flirt_data.append({"text": row["text"], "tone": row["tone"], "hobby": row["hobby"]})

        documents = [item["text"] for item in flirt_data]
        metadatas = [{"tone": item["tone"], "hobby": item["hobby"]} for item in flirt_data]

        #current_count = len(self.vectorstore._collection.get()["ids"])
        current_count = 0
        ids = [str(current_count + i) for i in range(len(documents))]
        self.vectorstore.add_texts(texts=documents, metadatas=metadatas, ids=ids)
import constant
import chromadb
from langchain_chroma import Chroma
from langchain.docstore.document import Document
from langchain_community.embeddings import GPT4AllEmbeddings
from chromadb.errors import InvalidCollectionException

from uuid import uuid4
from typing import List


def get_vector_store(documents: List[Document]):

    persistent_client = chromadb.PersistentClient(path="./Chroma")
    collection_name = constant.collection_name

    try:
        # Try to get the persistent collection, if success, ignores the documents argument for vector store creation
        collection = persistent_client.get_collection(collection_name)

    except InvalidCollectionException:
        # If not persistent collection, create a persistent colllection
        collection = persistent_client.create_collection(collection_name)
        collection.add(ids=[str(uuid4()) for _ in range(len(documents))], documents=documents)
    
    vector_store = Chroma(
        client=persistent_client,
        collection_name=collection_name,
        embedding_function=GPT4AllEmbeddings()
    )

    return vector_store
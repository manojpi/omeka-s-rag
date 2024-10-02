from langchain_community.document_loaders import FireCrawlLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

import os

from vector_store import get_vector_store
from constant import env_crawl_omeka_s, omeka_s_urls, retriever_num_of_returned_docs


def document_splitter_v_filter(documents):

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=300,
        chunk_overlap=30
    )

    document_splits = text_splitter.split_documents(documents)

    # Filter the complex metadata docs
    filtered_docs = []
    for document in document_splits:

        if isinstance(document, Document) and hasattr(document, "metadata"):
            clean_metadata = {k: v for k,v in document.metadata.items() if isinstance(v, (str, int, float, bool))}
            filtered_docs.append(Document(page_content=document.page_content, metadata=clean_metadata))
    
    return filtered_docs


def get_retriever():

    documents = []
    # Determine whether to crawl Omeka-s documentation or not

    if (bool(os.getenv(env_crawl_omeka_s))):
        
        documents_list = [FireCrawlLoader(api_key=os.getenv('FIRECRAWL_API_KEY'), url=url, mode='scrape').load() for url in omeka_s_urls]
        documents_list_flatten = [document for sublist in documents_list for document in sublist] # flatten the [[Docs]] to [Docs, ...]

        documents = document_splitter_v_filter(documents_list_flatten)
        os.environ[env_crawl_omeka_s] = "False"
    vector_store = get_vector_store(documents)

    return vector_store.as_retriever(search_kwargs={"k": retriever_num_of_returned_docs})

retriever = get_retriever()

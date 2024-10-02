app_name = "omeka-s-rag-bot"
collection_name = "omeka-s-rag-chroma"
local_llm = "llama3"
omeka_s_urls = [
    'https://omeka.org/s/docs/developer/api/',
    'https://omeka.org/s/docs/developer/api/php_api/',
    'https://omeka.org/s/docs/developer/api/rest_api/',
    'https://omeka.org/s/docs/developer/api/representations/',
    'https://omeka.org/s/docs/developer/api/api_reference/',
    'https://omeka.org/s/docs/developer/api/rest_api_reference/'    
]
env_crawl_omeka_s = "CRAWL_OMEKA_S"
env_tavily_api = "TAVILY_API_KEY"
retriever_num_of_returned_docs = 7
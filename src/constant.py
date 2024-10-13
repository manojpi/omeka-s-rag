app_name = "omeka-s-rag-bot"
collection_name = "omeka-s-rag-chroma"
local_llm = "llama3"
omeka_s_urls = ['https://omeka.org/s/docs/developer/', 
                'https://omeka.org/s/docs/developer/http://github.com/omeka/omeka-s-developer'
                'https://omeka.org/s/docs/developer/', 
                'https://omeka.org/s/docs/developer/whatsnew/', 
                'https://omeka.org/s/docs/developer/for_classic_developers/',
                'https://omeka.org/s/docs/developer/devpriorities/', 
                'https://omeka.org/s/docs/developer/api/', 
                'https://omeka.org/s/docs/developer/api/php_api/', 
                'https://omeka.org/s/docs/developer/api/rest_api/', 
                'https://omeka.org/s/docs/developer/api/representations/', 
                'https://omeka.org/s/docs/developer/api/api_reference/', 
                'https://omeka.org/s/docs/developer/api/rest_api_reference/', 
                'https://omeka.org/s/docs/developer/miscellaneous/acl/', 
                'https://omeka.org/s/docs/developer/miscellaneous/doctrine_orm/', 
                'https://omeka.org/s/docs/developer/miscellaneous/forms/', 
                'https://omeka.org/s/docs/developer/miscellaneous/internationalization/', 
                'https://omeka.org/s/docs/developer/configuration/',
                'https://omeka.org/s/docs/developer/configuration/authentication/', 
                'https://omeka.org/s/docs/developer/configuration/authorization/', 
                'https://omeka.org/s/docs/developer/configuration/metadata/', 
                'https://omeka.org/s/docs/developer/configuration/plugin_configuration/', 
                'https://omeka.org/s/docs/developer/plugins/', 
                'https://omeka.org/s/docs/developer/plugins/installing/', 
                'https://omeka.org/s/docs/developer/plugins/writing_plugins/',
                'https://omeka.org/s/docs/developer/plugins/development/']
env_crawl_omeka_s = "CRAWL_OMEKA_S"
env_tavily_api = "TAVILY_API_KEY"
retriever_num_of_returned_docs = 7
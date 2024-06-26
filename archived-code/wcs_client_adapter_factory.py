# import os
# import weaviate
# from abc import ABC, abstractmethod
# from weaviate.auth import AuthApiKey
# from importlib.metadata import version, PackageNotFoundError
# from typing import Optional

# def _get_weaviate_client_version() -> Optional[int]:
#     try:
#         client_version = version("weaviate-client")
#         major_version = int(client_version.split('.')[0])
#         if major_version in (3, 4):
#             return major_version
#         else:
#             return None
#     except PackageNotFoundError:
#         return None
      
# client_version = _get_weaviate_client_version()
# if client_version == 4:
#     from weaviate.classes import config, data
    
# WCS_URL = os.getenv("WCS_URL")
# WCS_API_KEY = os.getenv("WCS_API_KEY")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# WCS_COLLECTION_NAME = "QaAgentRagChunks"
# COLLECTION_TEXT_KEY = "chunk"

# class AbstractWcsClientAdapter(ABC):
#     def __init__(self):
#         self._wcs_client = None
        
#     @abstractmethod
#     def get_wcs_client(self):
#         pass
    
#     @abstractmethod
#     def connect(self):
#         pass

#     @abstractmethod
#     def close(self):
#         pass

#     @abstractmethod
#     def setup_collection(self):
#         pass

#     @abstractmethod
#     def count_entries(self):
#         pass

#     @abstractmethod
#     def insert_text_splits(self, text_splits):
#         pass

#     @abstractmethod
#     def retrieve_top_3_chunks(self, question):
#         pass

# class WcsClientV4Adapter(AbstractWcsClientAdapter):
#     def get_wcs_client(self):
#         return weaviate.connect_to_wcs(
#             cluster_url = WCS_URL,
#             auth_credentials=AuthApiKey(api_key = WCS_API_KEY),
#             headers={
#                 "X-OpenAI-Api-Key": OPENAI_API_KEY
#             }
#         )
        
#     def connect(self):
#         self._client = get_wcs_client()

#     def close(self):
#         if self._client:
#             self._client.close()

#     def setup_collection(self):
#         try:
#           self.connect()
#           if self._client.collections.exists(WCS_COLLECTION_NAME):
#               self._client.collections.delete(WCS_COLLECTION_NAME)  # Delete existing collection
          
#           self._client.collections.create(
#               name=WCS_COLLECTION_NAME,
#               properties=[
#                   config.Property(name=COLLECTION_TEXT_KEY, data_type=config.DataType.TEXT),
#                   config.Property(name="chunk_index", data_type=config.DataType.INT),
#               ],
#               # Todo: should this be declared in the indexer?
#               vectorizer_config=config.Configure.Vectorizer.text2vec_openai()
#           )
#         finally:
#           self.close()

#     def count_entries(self):
#         try:
#           self.connect()
#           response = self._client.collections.get(WCS_COLLECTION_NAME).aggregate.over_all(total_count=True)
#           return response.total_count
#         finally:
#           self.close()

#     def insert_text_splits(self, text_splits):
#         """Insert the text splits into the collection."""
#         try:
#           self.connect()
#           chunks_list = []
#           for i, chunk in enumerate(text_splits):
#               data_properties = {
#                   "chunk": chunk,
#                   "chunk_index": i
#               }
#               data_object = data.DataObject(properties=data_properties)
#               chunks_list.append(data_object)
#           self._client.collections.get(WCS_COLLECTION_NAME).data.insert_many(chunks_list)
#         finally:
#           self.close()

#     def retrieve_top_3_chunks(self, question):
#         top_k = 3
#         all_chunks = self._client.collections.get(WCS_COLLECTION_NAME)
#         retrieved_chunks = all_chunks.query.near_text(query=question, limit=top_k)
#         retrieved_chunks_list = [obj.properties['chunk'] for obj in retrieved_chunks.objects]
#         return retrieved_chunks_list

# class WcsClientV3Adapter(AbstractWcsClientAdapter):
#     def connect(self):
#         auth_config = weaviate.auth.AuthApiKey(api_key=WCS_API_KEY)
#         self._client = weaviate.Client(
#         url=WCS_URL,
#         auth_client_secret=auth_config,
#         additional_headers={  
#             "X-OpenAI-Api-Key": OPENAI_API_KEY
#         }
#         )

#     def close(self):
#         pass

#     def setup_collection(self):
#         try:
#             self.connect()
#             if self._client.schema.exists(WCS_COLLECTION_NAME):
#                 self._client.schema.delete_class(WCS_COLLECTION_NAME)
            
#             class_obj = {
#                 "class": WCS_COLLECTION_NAME,
#                 "properties": [
#                     {
#                         "name": "chunk",
#                         "dataType": ["text"],
#                     },
#                     {
#                         "name": "chunk_index",
#                         "dataType": ["int"],
#                     },
#                 ],
#                 "vectorizer": "text2vec-openai"
#             }

#             client.schema.create_class(class_obj)
#         finally:
#             self.close()

#     def count_entries(self):
#         pass

#     def insert_text_splits(self, text_splits):
#         pass

#     def retrieve_top_3_chunks(self, question):
#         pass


# class WcsClientAdapterFactory:
#     @staticmethod
#     def get_client_adapter():
#         client_version = _get_weaviate_client_version()
#         if client_version == 4:
#             return WcsClientV4Adapter()
#         elif client_version == 3:
#             return WcsClientV3Adapter()
#         else:
#             raise ValueError("Unsupported version of Weaviate client")
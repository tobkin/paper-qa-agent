import os
import weaviate
from weaviate.auth import AuthApiKey
from wcs_client_adapter import WcsClientAdapter

class NaiveWcsRetriever:
  def __init__(self):
    self._client = None
  
  def retrieve(self, question):
    retrieved_chunks_list = WcsClientAdapter.retrieve_top_3_chunks(question)
    formatted_chunks = "\n\n".join(chunk for chunk in retrieved_chunks_list)
    return formatted_chunks
  
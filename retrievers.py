import os
import weaviate
from weaviate.auth import AuthApiKey

_TOP_K = 3

class NaiveWcsRetriever:
  def __init__(self, collection_name):
    self._client = None
    self._collection_name = collection_name
  
  def retrieve(self, question):
    try:
      self._connect()
      all_chunks = self._client.collections.get(self._collection_name)
      retrieved_chunks = all_chunks.query.near_text(query=question, limit=_TOP_K)
      retrieved_chunks_list = [obj.properties['chunk'] for obj in retrieved_chunks.objects]
      formatted_chunks = "\n\n".join(chunk for chunk in retrieved_chunks_list)
      return formatted_chunks
    finally:
      self._close()
  
  # Todo: this is a DRY violation    
  def _connect(self):
      """Establish a connection to the Weaviate cluster."""
      self._client = weaviate.connect_to_wcs(
          cluster_url=os.getenv("WCS_URL"),
          auth_credentials=AuthApiKey(api_key=os.getenv("WCS_API_KEY")),
          headers={
              "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")
          }
      )
  
  # Todo: this is a DRY violation    
  def _close(self):
      """Close the Weaviate client connection."""
      if self._client:
          self._client.close()
import os
import weaviate
from weaviate.auth import AuthApiKey

class NaiveWcsRetriever:
  def __init__(self, vector_db):
    self._client = None
    self._vector_db = vector_db
  
  def retrieve(self, question):
    try:
      self._vector_db.connect()
      retrieved_chunks_list = self._vector_db.retrieve_top_3_chunks(question)
      formatted_chunks = "\n\n".join(chunk for chunk in retrieved_chunks_list)
      return formatted_chunks
    finally:
      self._vector_db.close()
  
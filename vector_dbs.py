import os
import weaviate
from weaviate.auth import AuthApiKey
from weaviate.classes import config, data

class WeaviateVectorDb: # Todo: rename to WcsClient
    def __init__(self, text_splits, collection_name):
        """
        Initialize the WeaviateVectorDatabase with specified text data and collection name.
        
        Args:
            text_splits (list of str): List of text chunks to be inserted into the database.
            collection_name (str): Name of the collection to create and use in Weaviate.
        """
        self.text_splits = text_splits 
        self.collection_name = collection_name
        self.client = None
        self._setup_collection()
        self._insert_data()
        
    def count_entries(self):
        """Count the total number of entries in the collection."""
        try:
          self._connect()
          response = self.client.collections.get(self.collection_name).aggregate.over_all(total_count=True)
          return response.total_count
        finally:
          self._close()
    
    # Todo: this is a DRY violation
    def _connect(self):
        """Establish a connection to the Weaviate cluster."""
        self.client = weaviate.connect_to_wcs(
            cluster_url=os.getenv("WCS_URL"),
            auth_credentials=AuthApiKey(api_key=os.getenv("WCS_API_KEY")),
            headers={
                "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")
            }
        )
   
    # Todo: this is a DRY violation 
    def _close(self):
        """Close the Weaviate client connection."""
        if self.client:
            self.client.close()
    
    def _setup_collection(self):
        """Setup or reset the collection in Weaviate."""
        try:
          self._connect()
          if self.client.collections.exists(self.collection_name):
              self.client.collections.delete(self.collection_name)  # Delete existing collection
          
          self.client.collections.create(
              name=self.collection_name,
              properties=[
                  config.Property(name="chunk", data_type=config.DataType.TEXT),
                  config.Property(name="chunk_index", data_type=config.DataType.INT),
              ],
              vectorizer_config=config.Configure.Vectorizer.text2vec_openai()
          )
        finally:
          self._close()
    
    def _insert_data(self):
        """Insert the text splits into the collection."""
        try:
          self._connect()
          chunks_list = []
          for i, chunk in enumerate(self.text_splits):
              data_properties = {
                  "chunk": chunk,
                  "chunk_index": i
              }
              data_object = data.DataObject(properties=data_properties)
              chunks_list.append(data_object)
          self.client.collections.get(self.collection_name).data.insert_many(chunks_list)
        finally:
          self._close()



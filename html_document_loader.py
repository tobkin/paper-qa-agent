import os
import requests

class HtmlDocumentLoader:
    """
    A class responsible for loading HTML documents from a specified URI.

    Attributes:
        uri (str): The URI from where the HTML document is loaded.
        cache_path (str): The path to the directory where the loaded documents are cached.
        doc (str): The content of the loaded HTML document as a string.

    Methods:
        load() -> str:
            Loads the HTML document from the specified URI into the `doc` attribute.
            Returns the content of the HTML document as a string.
    """

    def __init__(self, uri, cache_path):
        """
        Initializes the HtmlDocumentLoader with the specified URI and cache path.

        Args:
            uri (str): The URI from where the HTML document will be loaded.
            cache_path (str): The path to the directory where the loaded documents are cached.
        """
        self.uri = uri
        self.cache_path = cache_path
        self.doc = ""

    def load(self):
        """
        Loads the HTML document from the specified URI into the `doc` attribute.
        If caching is enabled and the document exists in cache, load it from there.

        Returns:
            str: The content of the HTML document.
        """
        # Create cache directory if it does not exist
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)

        # Create a hashed filename to store the document
        hash_filename = str(hash(self.uri))
        cached_file_path = os.path.join(self.cache_path, hash_filename)

        # Check if the document is cached and load it if yes
        if os.path.exists(cached_file_path):
            with open(cached_file_path, 'r', encoding='utf-8') as file:
                self.doc = file.read()
        else:
            # Fetch the document from the URI
            response = requests.get(self.uri)
            response.raise_for_status()  # Raises HTTPError for bad requests
            self.doc = response.text

            # Save the document to cache
            with open(cached_file_path, 'w', encoding='utf-8') as file:
                file.write(self.doc)

        return self.doc
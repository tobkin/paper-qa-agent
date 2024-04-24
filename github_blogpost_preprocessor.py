from bs4 import BeautifulSoup, SoupStrainer

class GithubBlogpostPreprocessor:
    """
    A class to preprocess HTML content from GitHub blog posts, focusing on specific
    parts of the post like the title, header, and content.
    """
    def __init__(self, html_content):
        """
        Initializes the preprocessor with HTML content.

        Args:
            html_content (str): The HTML content to be processed.
        """
        self.html_content = html_content

    def get_text(self):
        """
        Extracts and returns clean text from the post content, title, and header.

        Returns:
            str: Cleaned text from specified parts of the HTML content.
        """
        only_post_text = SoupStrainer(class_=["post-content", "post-title", "post-header"])
        soup = BeautifulSoup(self.html_content, "html.parser", parse_only=only_post_text)
        cleaned_text = soup.get_text()
        
        return cleaned_text

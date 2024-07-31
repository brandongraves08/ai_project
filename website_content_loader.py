import requests
from bs4 import BeautifulSoup
from langchain.schema import Document

class WebsiteContentLoader:
    def __init__(self, url: str):
        self.url = url

    def fetch_content(self) -> str:
        response = requests.get(self.url)
        response.raise_for_status()
        return response.text

    def process_content(self) -> Document:
        html = self.fetch_content()
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text(separator='\n', strip=True)
        return Document(page_content=text)

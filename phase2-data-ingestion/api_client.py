import requests
import os
from dotenv import load_dotenv

load_dotenv()

class OpenLibraryClient:
    BASE_URL = os.getenv("Base_URL")
    if not BASE_URL:
        raise ValueError("BASE_URL is not set in environment variables.")

    def __init__(self, rate_limit_delay: float = 1.0):
        self.delay = rate_limit_delay

    def _get(self, endpoint: str):
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url)

        if response.status_code != 200:
            return None

        return response.json()

    def search_author(self, author_name: str):
        data = self._get(f"/search/authors.json?q={author_name}")
        if not data:
            return None

        docs = data.get("docs", [])
        if not docs:
            return None

        return docs[0]["key"]

    def get_author_works(self, author_key: str):
        data = self._get(f"/authors/{author_key}/works.json")
        if not data:
            return []

        return data.get("entries", [])

    def get_work_editions(self, work_id: str):
        data = self._get(f"/works/{work_id}/editions.json")
        if not data:
            return []

        return data.get("entries", [])

    def get_valid_edition_data(self, work_id: str):
        editions = self.get_work_editions(work_id)

        for edition in editions:
            isbn_13 = edition.get("isbn_13")
            isbn_10 = edition.get("isbn_10")
            publish_date = edition.get("publish_date")

            isbn = None
            if isbn_13:
                isbn = isbn_13[0]
            elif isbn_10:
                isbn = isbn_10[0]

            if isbn and publish_date:
                return isbn, publish_date

        return None, None

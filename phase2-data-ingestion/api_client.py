import requests
import time


class OpenLibraryClient:
    BASE_URL = "https://openlibrary.org"

    def __init__(self, rate_limit=1):
        self.rate_limit = rate_limit  # seconds
        self.session = requests.Session()

    def _get(self, endpoint: str, params=None):
        url = f"{self.BASE_URL}{endpoint}"

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            time.sleep(self.rate_limit)  # respectful rate limiting
            return response.json()

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")

    # -----------------------------------------------------
    # Author Search
    # -----------------------------------------------------

    def search_author(self, author_name: str):
        data = self._get(
            "/search/authors.json",
            params={"q": author_name}
        )

        if not data.get("docs"):
            raise ValueError("Author not found.")

        return data["docs"][0]  # Take best match

    # -----------------------------------------------------
    # Fetch Works
    # -----------------------------------------------------

    def get_author_works(self, author_key: str, limit: int = 10):
        data = self._get(f"/authors/{author_key}/works.json")

        works = data.get("entries", [])
        return works[:limit]

    # -----------------------------------------------------
    # Fetch Work Details
    # -----------------------------------------------------

    def get_work_details(self, work_key: str):
        return self._get(f"{work_key}.json")
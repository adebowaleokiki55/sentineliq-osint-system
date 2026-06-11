from newsapi import NewsApiClient
from dotenv import load_dotenv
import os

load_dotenv()


class SearchEngine:

    def __init__(self):

        self.api = NewsApiClient(
            api_key=os.getenv("NEWS_API_KEY")
        )

    def search(self, query):

        try:

            response = self.api.get_everything(
                q=query,
                language="en",
                sort_by="relevancy",
                page_size=10
            )

            articles = response.get("articles", [])

            results = []

            for a in articles:

                if not a.get("url"):
                    continue

                results.append({
                    "title": a["title"],
                    "url": a["url"]
                })

            return results

        except Exception as e:

            print(e)

            return []
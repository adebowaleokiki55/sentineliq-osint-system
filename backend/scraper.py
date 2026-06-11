import trafilatura
import requests

class Scraper:

    def extract(self, url):

        try:
            downloaded = trafilatura.fetch_url(url)

            if not downloaded:
                return ""

            text = trafilatura.extract(downloaded)

            return text or ""

        except:
            return ""
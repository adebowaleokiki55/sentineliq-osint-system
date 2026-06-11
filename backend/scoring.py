import tldextract

class SourceScorer:

    def score(self, url):

        domain = tldextract.extract(url).registered_domain

        trusted = [
            "bbc.com", "reuters.com", "apnews.com",
            "who.int", "nature.com"
        ]

        if domain in trusted:
            return 1.0

        if domain.endswith(".gov") or domain.endswith(".edu"):
            return 0.9

        return 0.5
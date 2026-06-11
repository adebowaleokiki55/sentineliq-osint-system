from urllib.parse import urlparse


# -----------------------------
# SOURCE CREDIBILITY DATABASE
# -----------------------------
TRUST_SCORES = {
    # 🟣 Tier 1: Global Wire Agencies (highest reliability)
    "reuters.com": 0.97,
    "apnews.com": 0.97,
    "afp.com": 0.95,

    # 🟣 Tier 2: Public broadcasters
    "bbc.com": 0.95,
    "pbs.org": 0.93,
    "dw.com": 0.92,  # Deutsche Welle

    # 🔵 Tier 3: Major global news networks
    "cnn.com": 0.85,
    "bloomberg.com": 0.90,
    "cnbc.com": 0.85,
    "nytimes.com": 0.88,
    "washingtonpost.com": 0.87,
    "theguardian.com": 0.85,
    "wsj.com": 0.92,

    # 🟠 Tier 4: Regional / international outlets
    "aljazeera.com": 0.83,
    "sky.com": 0.80,
    "abcnews.go.com": 0.82,
    "globalnews.ca": 0.80,

    # 🟡 Tier 5: Nigerian mainstream media
    "punchng.com": 0.72,
    "vanguardngr.com": 0.72,
    "guardian.ng": 0.75,
    "premiumtimesng.com": 0.78,
    "thenationonlineng.net": 0.73,
    "dailytrust.com": 0.74,

    # 🟢 Tier 6: Lower reliability / tabloid-style outlets
    "dailymail.co.uk": 0.60,
    "thesun.co.uk": 0.55,
    "lindaikejisblog.com": 0.50,

    # ⚪ Default fallback
    "default": 0.50
}


# -----------------------------
# DOMAIN PARSER (SAFE)
# -----------------------------
def get_domain(url: str):

    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # remove www.
        if domain.startswith("www."):
            domain = domain.replace("www.", "")

        return domain

    except:
        return ""


# -----------------------------
# CREDIBILITY ENGINE
# -----------------------------
def credibility_score(url: str):

    domain = get_domain(url)

    if not domain:
        return TRUST_SCORES["default"]

    # 1. Exact match (best case)
    if domain in TRUST_SCORES:
        return TRUST_SCORES[domain]

    # 2. Safe subdomain match
    for key in TRUST_SCORES:
        if domain.endswith(key):
            return TRUST_SCORES[key]

    # 3. Unknown sources
    return TRUST_SCORES["default"]
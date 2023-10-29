

DATABASE_URLS = {
    'TAILSCALE': "postgresql://postgres:password@100.68.124.90:5432/reddit_scraper_1",
    'LOCAL': "postgresql://postgres:password@192.168.1.129:5432/reddit_scraper_1",
    'LOCALHOST': "postgresql://postgres:password@localhost:5432/reddit_scraper_1",
    # ... Add more access paths as needed
}

MAX_ATTEMPTS: int = 2
WAIT_BETWEEN_ATTEMPTS: int = 3
CONCURRENCEY_LIMIT: int = 6





URL_LIST: str = [
    "https://www.reddit.com/r/Jokes/",
    "https://www.reddit.com/r/explainlikeimfive/",
    "https://www.reddit.com/r/LifeProTips/",
    "https://www.reddit.com/r/TrueOffMyChest/",
    "https://www.reddit.com/r/talesfromtechsupport/",
    "https://www.reddit.com/r/AskUK/",
    "https://www.reddit.com/r/tifu/",
    "https://www.reddit.com/r/tifu/",
    "https://www.reddit.com/r/AmItheAsshole/",
    "https://www.reddit.com/r/legaladvice/",
    "https://www.reddit.com/r/whowouldwin/",
    "https://www.reddit.com/r/AskReddit/",
    "https://www.reddit.com/r/HFY/",
    "https://www.reddit.com/r/AskHistorians/",
    "https://www.reddit.com/r/talesfromretail/",
    "https://www.reddit.com/r/talesfromtechsupport/",
    "https://www.reddit.com/r/wouldyourather/",
    "https://www.reddit.com/r/stories/",
    "https://www.reddit.com/r/answers/"
]

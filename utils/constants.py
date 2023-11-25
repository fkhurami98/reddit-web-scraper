

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
    "https://old.reddit.com/r/Jokes/",
    "https://old.reddit.com/r/explainlikeimfive/",
    "https://old.reddit.com/r/LifeProTips/",
    "https://old.reddit.com/r/TrueOffMyChest/",
    "https://old.reddit.com/r/talesfromtechsupport/",
    "https://old.reddit.com/r/AskUK/",
    "https://old.reddit.com/r/tifu/",
    "https://old.reddit.com/r/tifu/",
    "https://old.reddit.com/r/AmItheAsshole/",
    "https://old.reddit.com/r/legaladvice/",
    "https://old.reddit.com/r/whowouldwin/",
    "https://old.reddit.com/r/AskReddit/",
    "https://old.reddit.com/r/HFY/",
    "https://old.reddit.com/r/AskHistorians/",
    "https://old.reddit.com/r/talesfromretail/",
    "https://old.reddit.com/r/talesfromtechsupport/",
    "https://old.reddit.com/r/wouldyourather/",
    "https://old.reddit.com/r/stories/",
    "https://old.reddit.com/r/answers/"
]

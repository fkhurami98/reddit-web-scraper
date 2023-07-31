import time
from bs4 import BeautifulSoup
from pprint import pprint
import random
import json
from playwright.sync_api import sync_playwright, TimeoutError
from urllib.parse import urlparse
import re


def get_reddit_page(url):
    """
    Visits a Reddit page using playwright and extracts the HTML.

    Args:
        url (str): The URL of the Reddit page for scraping.
        max_attempts (int, optional): The maximum number of attempts to load the page in case of timeouts. Defaults to 3.

    Returns:
        str: A string containing the HTML of the Reddit page, or None if the maximum attempts are exceeded.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(user_agent=get_random_user_agent())
        page = context.new_page()

        try:
            page.goto(
                url, timeout=60 * 1000
            )  # possibly increases time for page to load therfor providing more content??
        except TimeoutError:
            print("Page navigation timed out.")

        accept_button = page.wait_for_selector(
            "shreddit-interactable-element#accept-all-cookies-button button",
            timeout=60 * 1000,
        )

        accept_button.click()

        page.wait_for_load_state("networkidle")
        html = page.content()

        browser.close()

        filename = sanitize_url_for_filename(url)

        with open(f"data_{filename}.html", "w") as html_file:
            html_file.write(html)

        return html


def get_random_user_agent():
    """
    Gets a random user agent from a list of common user agents.

    Returns:
        str: A random user agent string.
    """
    # List of common user agents
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; MED-LX9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.99 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 9; Redmi 8A Build/PKQ1.190319.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.110 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/294.0.0.39.118;]",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 165.0.0.20.119 (iPhone11,8; iOS 13_7; pt_BR; pt-BR; scale=2.00; 828x1792; 252729634) NW/1",
        "Mozilla/5.0 (Linux; Android 10; BLA-L09 Build/HUAWEIBLA-L09S; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/112.0.5615.136 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/413.0.0.30.104;]",
    ]

    return random.choice(user_agents)


def sanitize_url_for_filename(url):
    """
    Sanitizes a URL to create a valid filename by replacing characters that are not allowed in filenames with underscores.

    Args:
        url (str): The URL to be sanitized.

    Returns:
        str: The sanitized filename.
    """
    # Use the urlparse function to get the path from the URL
    path = urlparse(url).path

    # Replace characters that are not allowed in filenames with underscores
    return re.sub(r"[^a-zA-Z0-9-_.]", "_", path)


if __name__ == "__main__":
    # List of Reddit URLs to scrape
    reddit_urls = [
        "https://www.reddit.com/r/worldnews/",
        "https://www.reddit.com/r/todayilearned/",
        "https://www.reddit.com/r/movies/",
        "https://www.reddit.com/r/showerthoughts/",
        # Add more URLs here as needed
    ]

    for url in reddit_urls:
        get_reddit_page(url)

# Accept button not found or timed out bug, still appearing even if it is found
# so unstable
# Sometimes json file is blank []?

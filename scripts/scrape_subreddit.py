from concurrent.futures import ThreadPoolExecutor
import time
from bs4 import BeautifulSoup
import random
import json
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
import re


def save_reddit_html_to_variable(url, output_file):
    """
    Saves the HTML content of a given Reddit URL to a file.

    Args:
        url (str): The Reddit URL to scrape.
        output_file (str): The filename to save the HTML content.

    Returns:
        str: The HTML content of the page.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(user_agent=get_random_user_agent())
        page = context.new_page()

        page.goto(
            url, timeout=60000
        )  # Increase timeout in case the page takes longer to load

        page.wait_for_load_state("networkidle")  # Wait for the page to load completely

        # Handle cookies button if it exists
        accept_button = page.query_selector(
            "button._1tI68pPnLBjR1iHcL7vsee._2iuoyPiKHN3kfOoeIQalDT._10BQ7pjWbeYP63SAPNS8Ts.HNozj_dKjQZ59ZsfEegz8"
        )
        if accept_button:
            accept_button.click()

        page.wait_for_load_state(
            "networkidle"
        )  # Wait for the page to load completely after accepting cookies

        page.evaluate(
            "window.scrollBy(0, window.innerHeight);"
        )  # Scroll down by the height of the viewport

        page.wait_for_load_state(
            "networkidle"
        )  # Wait for the page to load completely after scrolling down

        page.wait_for_timeout(1000)  # Wait for one second

        html_content = page.content()  # Get the entire HTML content of the page

        browser.close()  # Close the browser

    return html_content


def get_random_user_agent():
    """
    Gets a random user agent from a list of common user agents.

    Returns:
        str: A random user agent string.
    """
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; MED-LX9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.99 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 9; Redmi 8A Build/PKQ1.190319.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.110 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/294.0.0.39.118;]",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 165.0.0.20.119 (iPhone11,8; iOS 13_7; pt_BR; pt-BR; scale=2.00; 828x1792; 252729634) NW/1",
        "Mozilla/5.0 (Linux; Android 10; BLA-L09 Build/HUAWEIBLA-L09S; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/112.0.5615.136 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/413.0.0.30.104;]",
    ]
    return random.choice(user_agents)


def parse_reddit_html(html):
    """
    Parses the HTML of a Reddit page using BeautifulSoup and extracts post elements.

    Args:
        html (str): The HTML content of the Reddit page.

    Returns:
        list: A list of BeautifulSoup elements representing post elements.
    """
    soup = BeautifulSoup(html, "html.parser")
    post_elements = soup.select("shreddit-post")
    return post_elements


def extract_post_metadata(post_element):
    """
    Extracts post information from a BeautifulSoup element representing a post.

    Args:
        post_element (bs4.element.Tag): BeautifulSoup element representing a post.

    Returns:
        dict: A dictionary containing post information.
    """
    post_title_element = post_element.select_one('[slot="title"]')
    post_title = post_title_element.text.strip() if post_title_element else "N/A"

    permalink_element = post_element.get("permalink")
    permalink = (
        "https://www.reddit.com" + permalink_element if permalink_element else "N/A"
    )

    subreddit_elem = post_element.get("subreddit-prefixed-name")
    subreddit = subreddit_elem if subreddit_elem else "N/A"

    author_element = post_element.get("author")
    author = author_element if author_element else "N/A"

    comment_count_element = post_element.get("comment-count")
    comment_count = int(comment_count_element) if comment_count_element else 0

    post_score_element = post_element.get("score")
    post_score = int(post_score_element) if post_score_element else 0

    post_data = {
        "Post Title": post_title,
        "Permalink": permalink,
        "Subreddit": subreddit,
        "Author": author,
        "Number of Comments": comment_count,
        "Post Score": post_score,
    }

    return post_data


def sanitize_url_for_filename(url):
    """
    Sanitizes a URL to create a valid filename by replacing characters that are not allowed in filenames with underscores.

    Args:
        url (str): The URL to be sanitized.

    Returns:
        str: The sanitized filename.
    """
    path = urlparse(url).path  # Use the urlparse function to get the path from the URL
    return re.sub(
        r"[^a-zA-Z0-9-_.]", "_", path
    )  # Replace characters that are not allowed in filenames with underscores


def scrape_reddit_url(reddit_url, max_retry=10, retry_delay=3):
    """
    Scrapes a Reddit URL, extracts post information, and saves the results to a JSON file.

    Args:
        reddit_url (str): The Reddit URL to scrape.
        max_retry (int, optional): Maximum number of retry attempts. Defaults to 10.
        retry_delay (int, optional): Delay in seconds between retries. Defaults to 3.

    Returns:
        None
    """
    filename = f"subreddit_page_data/{sanitize_url_for_filename(reddit_url)}.json"

    retry_count = 0
    homepage_post_list = []

    while retry_count < max_retry:
        try:
            html_data = save_reddit_html_to_variable(reddit_url, output_file=filename)
            post_elements = parse_reddit_html(html_data)

            homepage_post_list = []
            for element in post_elements:
                post_data = extract_post_metadata(element)
                homepage_post_list.append(post_data)

            if homepage_post_list:
                break
        except Exception as e:
            print(f"An error occurred while scraping {reddit_url}: {e}")

        retry_count += 1
        print(f"Retry {retry_count}/{max_retry}. Retrying in {retry_delay} seconds...")
        time.sleep(retry_delay)

    if homepage_post_list:
        print(f"Scraped {reddit_url}:")
        with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(homepage_post_list, json_file, indent=4)
    else:
        print(f"Failed to scrape {reddit_url} even after retries.")


def scrape_reddit_urls_with_threads(urls, max_retry=10, retry_delay=3, num_threads=6):
    """
    Scrapes multiple Reddit URLs concurrently using threads.

    Args:
        urls (list): A list of Reddit URLs to scrape.
        max_retry (int, optional): Maximum number of retry attempts. Defaults to 10.
        retry_delay (int, optional): Delay in seconds between retries. Defaults to 3.
        num_threads (int, optional): Number of threads to use for concurrent scraping. Defaults to 4.

    Returns:
        None
    """
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(lambda url: scrape_reddit_url(url, max_retry, retry_delay), urls)


def scrape_subreddits():
    """
    Initiates the scraping process for a list of Reddit URLs.

    Returns:
        None
    """
    reddit_urls = [
        "https://www.reddit.com/r/Python/",
        "https://www.reddit.com/r/programming/",
        "https://www.reddit.com/r/badcode/",
        "https://www.reddit.com/r/javascript/",
        "https://www.reddit.com/r/announcements/",
        "https://www.reddit.com/r/science/",
        "https://www.reddit.com/r/Jokes/",
        "https://www.reddit.com/r/explainlikeimfive/",
        "https://www.reddit.com/r/LifeProTips/",
        "https://www.reddit.com/r/tifu/",
        "https://www.reddit.com/r/AskReddit/",
        "https://www.reddit.com/r/worldnews/",
    ]

    # Call the function to scrape Reddit URLs using threads
    scrape_reddit_urls_with_threads(reddit_urls)


if __name__ == "__main__":
    scrape_subreddits()

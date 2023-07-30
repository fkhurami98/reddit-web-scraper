import time
from bs4 import BeautifulSoup
from pprint import pprint
import random
import json
from playwright.sync_api import sync_playwright, TimeoutError
from urllib.parse import urlparse
import re

def get_reddit_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(user_agent=get_random_user_agent())
        page = context.new_page()

        try:
            page.goto(url, timeout=60 * 1000)  # Increase the timeout to 60 seconds
        except TimeoutError:
            print("Page navigation timed out.")

        try:
            accept_button = page.wait_for_selector(
                "shreddit-interactable-element#accept-all-cookies-button button",
                timeout=20 * 1000,
            )
            accept_button.click()
        except TimeoutError:
            print("Accept button not found or timed out.")

        page.wait_for_load_state("networkidle")
        html = page.content()

        browser.close()

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


def extract_individual_post_info(html_code):
    """
    Extracts individual post information from the HTML content.

    Args:
        html_code (str): The HTML code of an individual post.

    Returns:
        dict: A dictionary containing post information.
    """
    soup = BeautifulSoup(html_code, "html.parser")

    parent_div = soup.select_one("div.mb-sm.mb-xs.px-md.xs\\:px-0")

    if not parent_div:
        post_info = {
            "Opinions": "Post content not found. Likely to be blank",
        }
    else:
        post_text = parent_div.find_all("p")
        opinions = [paragraph.text.strip() for paragraph in post_text]
        post_info = {
            "Opinions": opinions,
        }

    return post_info

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


def scrape_reddit_url(url):
    """
    Scrapes data from a given Reddit URL.

    Args:
        url (str): The URL of the Reddit page to scrape.

    Returns:
        None
    """
    html = get_reddit_page(url)
    post_elements = parse_reddit_html(html)
    post_data_list = []

    for post_element in post_elements:
        post_data = extract_post_metadata(post_element)

        try:
            with open("posts_metadata.json", "r") as file:
                existing_post_data_list = json.load(file)
        except FileNotFoundError:
            existing_post_data_list = []

        permalink = post_data["Permalink"]
        print(f"Extracting HTML from {permalink}")
        html_content = get_reddit_page(permalink)
        data = extract_individual_post_info(html_content)
        post_data.update(data)
        pprint(post_data)
        time.sleep(30)

        post_data_list.append(post_data)

    combined_post_data_list = existing_post_data_list + post_data_list

    filename = sanitize_url_for_filename(url)  # Sanitize URL for use as a filename

    with open(f"data_{filename}.json", "w") as json_file:
        json.dump(combined_post_data_list, json_file, indent=4)


if __name__ == "__main__":
    # List of Reddit URLs to scrape
    reddit_urls = [
        "https://www.reddit.com",
        "https://www.reddit.com/r/python/",
        "https://www.reddit.com/r/AmItheAsshole/",
        # Add more URLs here as needed
    ]

    for url in reddit_urls:
        scrape_reddit_url(url)

#Accept button not found or timed out bug, still appearing even if it is found
# Get comments frm each 
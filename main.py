from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError
from pprint import pprint
import random
import json


def get_reddit_page(url):
    """
    Visits a reddit page using playwright and extracts the html.

    Args:
        url(str): The url of the reddit page for scraping.

    Returns:
        str: A string containing the html of the reddit page.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(user_agent=get_random_user_agent())
        page = context.new_page()

        page.goto(url)

        try:
            accept_button = page.wait_for_selector(
                "shreddit-interactable-element#accept-all-cookies-button button",
                timeout=30000,
            )
            accept_button.click()
        except TimeoutError:
            print("Accept button not found or timed out.")

        # Wait for the page to load after clicking the button
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
        html(str): The HTML content of the Reddit page.

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
        post_element(bs4.element.Tag): BeautifulSoup element representing a post.

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


if __name__ == '__main__':
    # Call the function to visit a reddit page
    html = get_reddit_page(url="https://www.reddit.com")
    
    # Parse the larger HTML page using BeautifulSoup
    post_elements = parse_reddit_html(html)
    
    # List to store the dictionaries of extracted post information
    post_data_list = []
    
    # Loop through all the post elements found
    for post_element in post_elements:
        # Extract post information
        post_data = extract_post_metadata(post_element)
    
        # Append the dictionary to the list
        post_data_list.append(post_data)
    
    # Print the extracted information for each post
    for post_data in post_data_list:
        print("--------------")
        for key, value in post_data.items():
            print(f"{key}: {value}")
    
    # Write post_data_list to a JSON file
    with open("posts_metadata.json", "w") as json_file:
        json.dump(post_data_list, json_file, indent=4)
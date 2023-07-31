from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
import json
import time

# Load the posts list from the JSON file
with open("_r_badcode_.json", "r") as json_file:
    posts = json.load(json_file)

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
            "Post content": "Post content not found. Likely to be blank, an image or a URL",
        }
    else:
        post_text = parent_div.find_all("p")
        opinions = [paragraph.text.strip() for paragraph in post_text]
        post_info = {
            "Post Content": opinions,
        }

    return post_info

def scrape_permalink_content(permalink):
    try:
        # Introduce some waiting time to avoid overloading the server

        # Send an HTTP GET request to the permalink URL
        response = requests.get(permalink)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        post_info = extract_individual_post_info(response.content)

        # Return the extracted information as needed
        return post_info

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while scraping {permalink}: {e}")
        return None

def main():
    # Use a ThreadPoolExecutor for concurrent scraping
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Loop through the list of posts and scrape the content for each permalink
        futures = [executor.submit(scrape_permalink_content, post["Permalink"]) for post in posts]

        # Wait for all the futures to complete
        for future, post in zip(futures, posts):
            post_info = future.result()
            if post_info:
                # Do something with the scraped content (e.g., store it in a database, save to a file, etc.)
                # You can also print the results to the console for testing purposes
                permalink = post["Permalink"]
                print(f"Post Info for {permalink}: {post_info}")
                print("-" * 50)

if __name__ == "__main__":
    main()
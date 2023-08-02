import os
import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor

def extract_individual_post_info(html_code):
    soup = BeautifulSoup(html_code, "html.parser")
    parent_div = soup.select_one("div.mb-sm.mb-xs.px-md.xs\\:px-0")

    if not parent_div:
        post_info = {
            "Post Content": "Post content not found. Likely to be blank, an image or a URL",
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
        response = requests.get(permalink)
        response.raise_for_status()

        post_info = extract_individual_post_info(response.content)
        return post_info

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while scraping {permalink}: {e}")
        return None

def process_json_file(json_file_path):
    with open(json_file_path, "r") as json_file:
        original_posts = json.load(json_file)
    
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(scrape_permalink_content, post["Permalink"]) for post in original_posts]

        for future, post in zip(futures, original_posts):
            post_info = future.result()
            if post_info:
                post.update(post_info)

    with open(json_file_path, "w") as json_file:
        json.dump(original_posts, json_file, indent=4)

def process_all_json_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            json_file_path = os.path.join(folder_path, filename)
            process_json_file(json_file_path)

def scrape_post_info():
    folder_path = 'subreddit_page_data'
    process_all_json_files(folder_path)
    

if __name__ == "__main__":
    scrape_post_info()

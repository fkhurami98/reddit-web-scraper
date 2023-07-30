from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def get_reddit_homepage():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36")
        page = context.new_page()

        page.goto("https://www.reddit.com")
        page.wait_for_load_state("networkidle")

        # Click on the "Accept all" button with the specified ID
        button_selector = 'shreddit-interactable-element#accept-all-cookies-button button'
        timeout_ms = 10000  # 10 seconds
        page.click(button_selector, timeout=timeout_ms)

        # Wait for the page to load after clicking the button
        page.wait_for_load_state("networkidle")

        html = page.content()

        browser.close()

        return html

# Call the function to get the Reddit homepage
html = get_reddit_homepage()

# Write the HTML to a file
with open('homepage.html', 'w') as f:
    f.write(html)

# Parse the larger HTML page using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find all elements with the shreddit-post class (the provided HTML snippet)
post_elements = soup.select('shreddit-post')

# Loop through all the post elements found
for post_element in post_elements:
    # Extracting post details
    post_title_elem = post_element.select_one('[slot="title"]')
    post_title = post_title_elem.text.strip() if post_title_elem else "N/A"

    permalink_elem = post_element.get('permalink')
    permalink = "https://www.reddit.com" + permalink_elem if permalink_elem else "N/A"

    subreddit_elem = post_element.get('subreddit-prefixed-name')
    subreddit = subreddit_elem if subreddit_elem else "N/A"

    author_elem = post_element.get('author')
    author = author_elem if author_elem else "N/A"

    comment_count_elem = post_element.get('comment-count')
    comment_count = int(comment_count_elem) if comment_count_elem else 0

    post_score_elem = post_element.get('score')
    post_score = int(post_score_elem) if post_score_elem else 0

    # Printing the extracted information for each post
    print("--------------")
    print("Post Title:", post_title)
    print("Permalink:", permalink)
    print("Subreddit:", subreddit)
    print("Author:", author)
    print("Number of Comments:", comment_count)
    print("Post Score:", post_score)

# Separator between snippets
print("--------------")

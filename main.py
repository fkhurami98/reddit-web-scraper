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



html = get_reddit_homepage()

with open('homepage.html', 'w') as f:
    f.write(html)

# Parse the larger HTML page using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find all elements with the shreddit-post class (the provided HTML snippet)
post_elements = soup.find_all('shreddit-post')

# Loop through all the post elements found
for post_element in post_elements:
    # Convert the element back to a string representation
    extracted_html_snippet = str(post_element)

    soup_post = BeautifulSoup(extracted_html_snippet, 'html.parser')

    # Extracting post details
    post_title_elem = soup_post.find('h3', {'class': '_eYtD2XCVieq6emjKBH3m'})
    post_title = post_title_elem.text.strip() if post_title_elem else "N/A"

    # Extracting permalink to full post
    permalink_elem = soup_post.find('a', {'class': 'SQnoC3ObvgnGjWt90zD9Z'})
    permalink = "https://www.reddit.com" + permalink_elem['href'] if permalink_elem else "N/A"
    subreddit = permalink.split('/')[4] if permalink != "N/A" else "N/A"

    # Extracting post author
    author_elem = soup_post.find('a', class_='_2tbHP6ZydRpjI44J3syuqC _23wugcdiaj44hdfugIAlnX oQctV4n0yUb0uiHDdGnmE')
    author = author_elem.text if author_elem else "N/A"

    # Extracting the number of comments
    comment_count_elem = soup_post.find('span', {'class': 'FHCV02u6Cp2zYL0fhQPsO'})
    comment_count = int(comment_count_elem.text.split()[0]) if comment_count_elem else 0

    post_score_elem = soup_post.find('div', {'class': '_1rZYMD_4xY3gRcSS3p8ODO'})
    post_score = int(post_score_elem.text) if post_score_elem else 0

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

#wikipedia_api.py
import requests
import time


# Base URL for the Wikipedia API
WIKI_API_URL = "https://en.wikipedia.org/w/api.php"

def get_links_from_article(title):
    """
    Fetches all internal links from a given Wikipedia article.
    Handles potential network errors silently for Streamlit.
    """
    params = {
        "action": "query",
        "titles": title,
        "prop": "links",
        "pllimit": "max",
        "format": "json"
    }
    try:
        response = requests.get(WIKI_API_URL, params=params, timeout=10).json()
        pages = response.get("query", {}).get("pages", {})
        for page_id in pages:
            links = pages[page_id].get("links", [])
            return [link["title"] for link in links if "title" in link]
    except requests.exceptions.RequestException:
        return []

def article_exists(title):
    """
    Checks if a Wikipedia article with the given title exists.
    Includes retries with exponential backoff for transient API errors.
    """
    params = {
        "action": "query",
        "titles": title,
        "format": "json"
    }

    max_retries = 3 # Number of times to retry the API call
    for attempt in range(max_retries):
        try:
            # Small base delay to be polite to the API
            time.sleep(0.05)
            # Exponential backoff for retries: 0s, 2s, 4s, etc.
            if attempt > 0:
                print(f"Retrying article_exists for '{title}' (Attempt {attempt + 1}/{max_retries})...")
                time.sleep(2 ** attempt)

            response = requests.get(WIKI_API_URL, params=params, timeout=10)
            # Raise an HTTPError for bad responses (4xx or 5xx)
            response.raise_for_status()

            pages = response.json().get("query", {}).get("pages", {})
            # Wikipedia API returns a page_id of -1 if the article does not exist
            # Also handle cases where 'pages' might be empty for very invalid titles
            return not (any(page_id == "-1" for page_id in pages.keys()) or not pages)

        except requests.exceptions.RequestException as e:
            # This catches network errors, timeouts, and HTTP errors (like 429, 500)
            print(f"API Error on attempt {attempt + 1} for '{title}': {e}")
            if attempt == max_retries - 1:
                # If all retries fail, then we genuinely couldn't verify.
                # It's safer to return False here as we cannot confirm existence.
                # This 'False' might be cached, but only after multiple failures.
                print(f"Failed to verify existence for '{title}' after {max_retries} attempts.")
                return False
        except Exception as e:
            # Catch any other unexpected errors that aren't request-related
            print(f"An unexpected error occurred for '{title}': {e}")
            return False # Non-request errors are also considered failure to verify

    return False

def normalize_title(title):
    """
    Wikipedia articles take _ instead of spaces in their URLs.
    Normalizes a Wikipedia article title by stripping whitespace and replacing spaces with underscores.
    """
    return title.strip().replace(" ", "_")
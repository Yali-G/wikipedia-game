import requests

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
    """
    params = {
        "action": "query",
        "titles": title,
        "format": "json"
    }
    try:
        response = requests.get(WIKI_API_URL, params=params, timeout=10).json()
        pages = response.get("query", {}).get("pages", {})
        return not any(page_id == "-1" for page_id in pages)
    except requests.exceptions.RequestException:
        return False

def normalize_title(title):
    """
    Wikipedia articles take _ instead of spaces in their URLs.
    Normalizes a Wikipedia article title by stripping whitespace and replacing spaces with underscores.
    """
    return title.strip().replace(" ", "_")
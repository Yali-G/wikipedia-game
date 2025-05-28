#wikipedia_game_player.py
from collections import deque
from wikipedia_api import get_links_from_article, article_exists, normalize_title

def wikipedia_game_player(start_article, end_article, max_depth, max_articles_to_check):
    """
    Generator function to play the Wikipedia game. It yields status updates
    and the current path as it explores the Wikipedia graph.

    Args:
        start_article (str): The title of the starting Wikipedia article.
        end_article (str): The title of the destination Wikipedia article.
        max_depth (int): The maximum number of links to traverse (depth of search).
        max_articles_to_check (int): The maximum number of articles to process.

    Yields:
        tuple: A tuple (status_message: str, current_path_list: list).
    """
    start_article_norm = normalize_title(start_article)
    end_article_norm = normalize_title(end_article)

    # Check to see that both articles exist before starting the game
    yield f"Checking if '{start_article}' exists...", []
    if not article_exists(start_article_norm):
        yield f"Error: Starting article '{start_article}' does not exist on Wikipedia.", []
        return

    yield f"Checking if '{end_article}' exists...", []
    if not article_exists(end_article_norm):
        yield f"Error: Destination article '{end_article}' does not exist on Wikipedia.", []
        return

    # If start and end are the same don't bother with BFS
    if start_article_norm.lower() == end_article_norm.lower():
        yield f"Start and target are the same! Path found.", [start_article_norm]
        return

    # Initialize BFS data structures
    # Queue stores (current_article_title, path_to_current_article, current_depth)
    queue = deque([(start_article_norm, [start_article_norm], 0)])
    visited = {start_article_norm}
    articles_processed = 0

    # yield f"Starting Wikipedia Game from '{start_article}' to '{end_article}'...", [start_article_norm]
    # yield f"Config: Max Depth={max_depth}, Max Articles to Check={max_articles_to_check}", [start_article_norm]

    # BFS loop
    while queue:
        current_article, path, depth = queue.popleft()
        articles_processed += 1

        # Yield progress updates to Streamlit
        status_message = f"Exploring: '{current_article.replace('_', ' ')}' (Depth: {depth}, Processed: {articles_processed})"
        yield status_message, path # Yield current path to show progress

        # Check if max depth is reached
        # If the depth exceeds max_depth, skip further processing for this branch
        if depth >= max_depth:
            continue

        # Check if max articles to check is reached
        # If the articles processed exceeds max articles, skip further processing for this branch
        if articles_processed >= max_articles_to_check:
            yield f"Reached maximum articles to check ({max_articles_to_check}). Aborting search.", path
            break

        # Get links from the current article
        links = get_links_from_article(current_article)

        for link in links:
            normalized_link = normalize_title(link)

            # Check if the destination article is found
            # If found then yield the path and exit
            if normalized_link.lower() == end_article_norm.lower():
                final_path = path + [end_article_norm]
                yield f"Path found! Reached '{end_article.replace('_', ' ')}' in {len(final_path)-1} steps!", final_path
                return

            # If the link has not been visited, add it to the queue
            if normalized_link not in visited:
                visited.add(normalized_link)
                new_path = path + [normalized_link]
                queue.append((normalized_link, new_path, depth + 1))

    # If the loop finishes and no path was found
    yield f"No path found from '{start_article}' to '{end_article}' within {max_depth} steps or {max_articles_to_check} articles processed.", path
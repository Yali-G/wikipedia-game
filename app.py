# app.py
import streamlit as st
from wikipedia_game_player import wikipedia_game_player
import time
        
def formatPath(path):
    """
    Formats the path for display in Streamlit.
    Converts titles to clickable links.
    """
    formatted_path = []
    for i, title in enumerate(path):
        wiki_url_title = title.replace(' ', '_')
        formatted_path.append(f"**Step {i+1}:** [{title.replace('_', ' ')}](https://en.wikipedia.org/wiki/{wiki_url_title})")
    return "\n".join(formatted_path)

st.set_page_config(page_title="Wikipedia Game", layout="centered")

st.title("Wikipedia Game")

st.write("Find the shortest path between two Wikipedia articles!")

# User inputs
start_input = st.text_input("Start Article", value="Start", help="Enter the title of the starting Wikipedia article (e.g., 'Pear').")
target_input = st.text_input("Target Article", value="Finish", help="Enter the title of the destination Wikipedia article (e.g., 'Benjamin Franklin').")

# Controls for max_depth and max_articles_to_check
col1, col2 = st.columns(2)
with col1:
    max_depth_val = st.slider("Max Search Depth", min_value=1, max_value=7, value=4, step=1, help="Limits how many links deep the search goes.")
with col2:
    max_articles_val = st.slider("Max Articles to Check", min_value=100, max_value=5000, value=2000, step=100, help="Limits the maximum number of articles to be processed.")

if st.button("Start Game 🚀"):
    
    # Placeholders for dynamic updates
    status_placeholder = st.empty()
    path_placeholder = st.empty()
    
    #initialize the current path list for display
    current_path_list = []

    # Run the game generator and update the UI dynamically
    for status_message, current_path_update in wikipedia_game_player(start_input, target_input, max_depth_val, max_articles_val):
        status_placeholder.info(status_message)
        current_path_list = current_path_update 
        
        # Display the current path with clickable links
        if current_path_list:
            path_placeholder.markdown(formatPath(current_path_list))
        else:
            path_placeholder.empty()

        # Add a small delay for smoother visualization
        time.sleep(0.1)

    st.success("Game finished!")
    
    # Display final path if it exists
    if current_path_list and isinstance(current_path_list, list) and len(current_path_list) > 1:
        st.write(f"Final Path found in {len(current_path_list)-1} steps:")
        st.markdown(formatPath(current_path_list))
    elif current_path_list and isinstance(current_path_list, list) and len(current_path_list) == 1:
        st.write(f"Start and target are the same: {current_path_list[0].replace('_', ' ')}")
    else:
        st.warning("Could not find a path based on your criteria.")
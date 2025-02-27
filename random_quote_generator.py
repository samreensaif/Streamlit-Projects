import streamlit as st
import requests
import json

def get_random_quote():
    """Fetch a random quote from the Quotable API"""
    try:
        response = requests.get("https://zenquotes.io/api/random")
        if response.status_code == 200:
            data = response.json()  # data is a list of dictionaries
            quote_data = data[0]  # Extract the first (and only) quote
            return {
                "content": quote_data["q"],  # "q" contains the quote text
                "author": quote_data["a"]    # "a" contains the author's name
            }
        else:
            return {
                "content": "Failed to fetch quote",
                "author": "Error"
            }
    except Exception as e:
        return {
            "content": "An error occurred",
            "author": str(e)
        }

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Random Quote Generator",
        page_icon="📚",
        layout="centered"
    )
    
    # Custom CSS with more specific selectors
    st.markdown("""
        <style>
        /* Main background */
        .stApp {
            background: linear-gradient(to right bottom, #4B0082, #800080);
        }
        
        /* Container styling */
        div[data-testid="stVerticalBlock"] {
            background-color: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            backdrop-filter: blur(5px);
            margin-bottom: 20px;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        
        /* Quote container */
        .quote-container {
            display: flex;
            flex-direction: column;
            padding: 20px;
            margin: 10px 0;
        }
        
        /* Quote styling */
        div.quote-text {
            color: yellow !important;
            font-size: 40px !important;
            text-align: center !important;
            margin: 20px 0 !important;
            padding: 20px !important;
            font-weight: bold !important;
            line-height: 1.4 !important;
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
        }
        
        /* Author styling */
        div.author-text {
            color: #FFB6C1 !important;
            font-size: 24px !important;
            text-align: right !important;
            padding: 10px 20px !important;
            margin: 0 !important;
            font-style: italic !important;
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
        }
        
        /* Button styling */
        .stButton>button {
            background-color: #FF69B4 !important;
            color: white !important;
            border: none !important;
            padding: 10px 24px !important;
            border-radius: 5px !important;
            transition: all 0.3s ease !important;
            width: 200px !important;
        }
        
        .stButton>button:hover {
            background-color: #FF1493 !important;
            transform: scale(1.05);
        }
        
        /* Title and text styling */
        h1, .title {
            color: white !important;
            font-weight: bold !important;
        }
        
        p {
            color: #F0F8FF !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Add title and description
    st.title("✨ Random Quote Generator")
    st.write("Click the button below to get inspired by a random quote!")
    
    # Add a button to generate new quotes
    if st.button("Generate Quote"):
        quote = get_random_quote()
        
        # Wrap quote and author in a container
        st.markdown(
            f'''
            <div class="quote-container">
                <div class="quote-text">"{quote["content"]}"</div>
                <div class="author-text">― {quote["author"]}</div>
            </div>
            ''', 
            unsafe_allow_html=True
        )
    
    # Add footer with custom styling
    st.markdown("<hr style='border-color: rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
    st.markdown(
        '<div style="color: #DDA0DD; text-align: center; font-size: 14px;">Data provided by '
        '<a style="color: #FFB6C1; text-decoration: none; font-weight: bold;" '
        'href="https://zenquotes.io/">ZenQuotes API</a></div>', 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

# interactive_scraper.py

import requests
from bs4 import BeautifulSoup
import streamlit as st

st.set_page_config(page_title="Interactive Web Scraper", layout="centered")

st.title("🕸️ Interactive Web Scraper")
st.markdown("Enter a website URL and HTML tag to extract information interactively!")

# --- Default values for testing ---
default_url = "https://quotes.toscrape.com"
default_tag = "span"

# --- Input from user ---
url = st.text_input("🔗 Website URL:", default_url)
tag = st.text_input("🏷️ HTML Tag to Scrape (e.g. p, h1, span, a):", default_tag)

def scrape_website(url, tag):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        elements = soup.find_all(tag)
        result = [el.get_text(strip=True) for el in elements if el.get_text(strip=True)]
        return result
    except Exception as e:
        return f"❌ Error: {e}"

# --- Button to trigger scraping ---
if st.button("🔍 Scrape Now"):
    with st.spinner("Scraping..."):
        output = scrape_website(url, tag)
        if isinstance(output, list):
            if output:
                st.success(f"✅ Found {len(output)} `{tag}` tags.")
                for i, content in enumerate(output[:50], 1):
                    st.markdown(f"**{i}.** {content}")
                if len(output) > 50:
                    st.info("📌 Showing only first 50 results.")
            else:
                st.warning(f"No `{tag}` elements found on this page.")
        else:
            st.error(output)


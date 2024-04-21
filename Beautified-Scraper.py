import streamlit as st
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import os

def scrape_url(url):
    # Set up Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Load the webpage
        driver.get(url)
        time.sleep(2)  # Wait for the page to load

        # Get the page source
        page_source = driver.page_source

        # Parse the HTML content
        soup = BeautifulSoup(page_source, "html.parser")

        # Extract the title of the page
        title = soup.title.string.strip() if soup.title else "N/A"

        # Extract the headings (h1 to h6) from the page
        headings = [heading.get_text(strip=True) for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])]

        # Extract the paragraphs from the page
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]

        # Extract the links from the page
        links = [link.get("href") for link in soup.find_all("a")]

        return title, headings, paragraphs, links

    except Exception as e:
        st.error(f"Error occurred while scraping: {e}")
        return None, None, None, None

    finally:
        # Close the WebDriver
        driver.quit()

def save_to_txt(title, headings, paragraphs, links, url_to_scrape):
    formatted_data = f"Title:\n{title}\n\n"
    formatted_data += "Headings:\n" + "\n".join(f"- {heading}" for heading in headings) + "\n\n"
    formatted_data += "Paragraphs:\n" + "\n\n".join(paragraphs) + "\n\n"
    formatted_data += "Links:\n" + "\n".join(f"- {link}" for link in links)

    domain = get_domain_name(url_to_scrape)
    
    # Replace or remove invalid characters from the title
    valid_title = re.sub(r'[\\/*?:"<>|]', '_', title)  # Replace invalid characters with '_'
    # OR
    # valid_title = re.sub(r'[\\/*?:"<>|]', '', title)  # Remove invalid characters

    filename = f"{valid_title}.txt" if valid_title else f"{domain}.txt"

    filepath = os.path.join(r"D:\Python-Tools\Tools\Multi-Scraper", filename)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(formatted_data)
    st.success(f"Scraped data saved to {filepath}")

def get_domain_name(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Remove the 'www.' prefix if present
    if domain.startswith('www.'):
        domain = domain[4:]

    # Extract the domain name without the TLD
    domain_parts = domain.split(".")
    if len(domain_parts) >= 2:
        domain_name = domain_parts[0]
        if domain_name:
            return domain_name
        else:
            return "default"
    else:
        if domain:
            return domain
        else:
            return "default"

if __name__ == "__main__":
    st.title("Web Scraping with Streamlit")

    url_to_scrape = st.text_input("Enter a URL to scrape:")

    if st.button("Scrape"):
        if url_to_scrape:
            st.info("Scraping in progress...")
            title, headings, paragraphs, links = scrape_url(url_to_scrape)

            if title:
                st.success("Scraping completed successfully!")
                st.write("Please check your terminal for the scraped data.")
                print(f"Title: {title}")
                print("Headings:")
                print(headings)
                print("Paragraphs:")
                print(paragraphs)
                print("Links:")
                print(links)
                save_to_txt(title, headings, paragraphs, links)
            else:
                st.error("Failed to scrape the URL.")
        else:
            st.warning("Please enter a URL to scrape.")

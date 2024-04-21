import streamlit as st
import requests
import time
import os
from urllib.parse import urlparse
import re

def scrape_url(url):
    start_time = time.time()  # Record the start time

    # Add 'http://' to the URL if it doesn't start with 'http://' or 'https://'
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    response = requests.get(url)

    elapsed_time = time.time() - start_time  # Calculate the elapsed time

    # Check if the request was successful and the elapsed time is within the limit
    if response.status_code == 200 and elapsed_time <= 6:
        return response.text
    elif elapsed_time > 6:
        print(f"Skipping {url} due to exceeding the time limit (elapsed time: {elapsed_time:.2f} seconds)")
    else:
        print(f"Failed to retrieve data from {url}: {response.status_code}")
    return None

def save_results_to_file(result, url):
    domain = get_domain_name(url)
    title = extract_title(result)
    filename = f"{title}.txt" if title else f"{domain}.txt"
    filepath = os.path.join(r"D:\Python-Tools\Tools\Multi-Scraper", filename)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(result)
    print(f"Scraped data saved to {filepath}")

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

def extract_title(html):
    title_pattern = r'<title>(.*?)</title>'
    match = re.search(title_pattern, html, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def main():

    url_to_scrape = st.text_input("Enter a URL to scrape:")

    if st.button("Scrape"):
        if url_to_scrape:
            st.info("Scraping in progress...")
            scraped_data = scrape_url(url_to_scrape)

            if scraped_data is not None:
                st.success("Scraping completed successfully!")
                print("Scraped data:")
                print(scraped_data)

                save_results_to_file(scraped_data, url_to_scrape)
                st.write("Scraped data saved to a text file.")
            else:
                st.error("Failed to scrape the URL.")
        else:
            st.warning("Please enter a URL to scrape.")

if __name__ == "__main__":
    main()
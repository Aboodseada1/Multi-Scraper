import streamlit as st
import importlib

def main():

    with st.sidebar:
        script_options = ["ChromeDriver Scraper", "Raw-Scraper"]
        selected_script = st.radio("Select a script", script_options)

    if selected_script == "ChromeDriver Scraper":
        st.title("ChromeDriver Scraper")
        beautified_scraper = importlib.import_module("Beautified-Scraper")

        url_to_scrape = st.text_input("Enter a URL to scrape:")

        if st.button("Scrape"):
            if url_to_scrape:
                st.info("Scraping in progress...")
                title, headings, paragraphs, links = beautified_scraper.scrape_url(url_to_scrape)

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
                    beautified_scraper.save_to_txt(title, headings, paragraphs, links, url_to_scrape)
                else:
                    st.error("Failed to scrape the URL.")
            else:
                st.warning("Please enter a URL to scrape.")

    elif selected_script == "Raw-Scraper":
        st.title("Raw Scraper")
        raw_scraper = importlib.import_module("Raw-Scraper")
        raw_scraper.main()

if __name__ == "__main__":
    main()
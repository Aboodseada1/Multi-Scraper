import click
import importlib
from . import Beautified_Scraper
from . import Raw_Scraper

@click.command(help="Multi-Scraper CLI tool")
@click.option('--raw', is_flag=True, help='Use raw scraper')
@click.option('--driver', is_flag=True, help='Use ChromeDriver scraper')
@click.option('--website', required=True, help='Website URL to scrape')
def main(raw, driver, website):
    """
    Multi-Scraper CLI tool
    
    USAGE:
    multi-scraper --raw --website <website_url>
    multi-scraper --driver --website <website_url>
    """

    if raw:
        Raw_Scraper.main(website)
    elif driver:
        Beautified_Scraper.main(website)
    else:
        click.echo("Please specify either '--raw' or '--driver' option.")

if __name__ == '__main__':
    main()

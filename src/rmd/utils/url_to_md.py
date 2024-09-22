import requests
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urljoin

from rmd.core.log import logger
from rmd.core.file_handler import FileHandler

class WebsiteToMarkdownConverter:
    def __init__(self, url, output_file):
        self.url = url
        self.output_file = output_file
        self.html_content = ""
        self.markdown_content = ""

    def fetch_url(self):
        """Fetch the content of the given URL."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.html_content = response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching URL: {e}")
            raise

    def html_to_markdown(self):
        """Convert HTML content to Markdown."""
        soup = BeautifulSoup(self.html_content, 'html.parser')
        self.markdown_content = ""

        # Extract title
        title = soup.title.string if soup.title else "Untitled"
        self.markdown_content += f"# {title}\n\n"

        # Process main content
        for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'img']):
            if element.name.startswith('h'):
                level = int(element.name[1])
                self.markdown_content += f"{'#' * level} {element.text.strip()}\n\n"
            elif element.name == 'p':
                self.markdown_content += f"{element.text.strip()}\n\n"
            elif element.name == 'a':
                href = urljoin(self.url, element.get('href', ''))
                self.markdown_content += f"[{element.text.strip()}]({href})"
            elif element.name == 'img':
                src = urljoin(self.url, element.get('src', ''))
                alt = element.get('alt', 'Image')
                self.markdown_content += f"![{alt}]({src})\n\n"

    def save_markdown(self):
        """Save the Markdown content to a file."""
        FileHandler.save_markdown(self.markdown_content, self.output_file)
        logger.info(f"Markdown saved to {self.output_file}")

    def convert(self):
        """Main method to handle the website to Markdown conversion process."""
        try:
            self.fetch_url()
            self.html_to_markdown()
            self.save_markdown()
            logger.info("Conversion completed successfully")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

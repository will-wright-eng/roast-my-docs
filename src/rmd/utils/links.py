import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

from rmd.core.config import file_paths, settings
from rmd.core.file_handler import FileHandler
from rmd.core.log import logger


class AsyncDocumentationCrawler:
    def __init__(self, start_url, target_domain):
        self.start_url = start_url
        self.target_domain = target_domain
        self.visited_urls = set()
        self.to_visit = asyncio.Queue()
        self.results_file = file_paths.extracted_urls

    async def crawl(self, max_urls=settings.MAX_LINKS):
        await self.to_visit.put(self.start_url)

        async with aiohttp.ClientSession() as session:
            while not self.to_visit.empty() and len(self.visited_urls) < max_urls:
                url = await self.to_visit.get()
                await self.crawl_url(session, url)

        logger.info(f"Crawl completed. Visited {len(self.visited_urls)} unique URLs.")

    async def crawl_url(self, session, url):
        if url in self.visited_urls:
            return

        self.visited_urls.add(url)
        logger.info(f"Crawling: {url}")

        try:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                content = await response.text()

            soup = BeautifulSoup(content, "html.parser")

            # Extract metadata
            title = soup.title.string if soup.title else "No title"
            description = soup.find("meta", attrs={"name": "description"})
            description = description["content"] if description else "No description"

            # Save result
            result = {"url": url, "title": title, "description": description}
            await self.save_result(result)

            # Find new links
            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link["href"])
                parsed_url = urlparse(full_url)

                if parsed_url.netloc == self.target_domain and not parsed_url.fragment:
                    clean_url = parsed_url._replace(fragment="").geturl()
                    if clean_url not in self.visited_urls:
                        await self.to_visit.put(clean_url)

        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logger.error(f"Error crawling {url}: {e}")

        await asyncio.sleep(1)  # Be polite to the server

    async def save_result(self, result):
        async with asyncio.Lock():
            FileHandler.append_jsonl(result, self.results_file)


async def main():
    start_url = (
        input("Enter the starting URL for the documentation: ")
        or "https://typer.tiangolo.com/"
    )
    target_domain = urlparse(start_url).netloc

    crawler = AsyncDocumentationCrawler(start_url, target_domain)
    await crawler.crawl()

import asyncio
from typing import Any, Dict, List, AsyncIterator

import aiohttp

from rmd.core.log import logger
from rmd.core.config import settings
from rmd.core.file_handler import FileHandler


class FirecrawlAPI:
    def __init__(self, api_token: str):
        self.base_url = "https://api.firecrawl.dev/v0"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }

    async def scrape_url(self, session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
        payload = {
            "url": url,
            "pageOptions": {
                "includeHtml": True,
                "onlyMainContent": True,
            },
            "extractorOptions": {
                "mode": "markdown",
            },
        }

        try:
            async with session.post(f"{self.base_url}/scrape", json=payload) as response:
                response.raise_for_status()
                data = await response.json()
                print(f"Successfully scraped: {url}")
                return {"url": url, "data": data}
        except aiohttp.ClientError as e:
            print(f"Error occurred while scraping {url}: {str(e)}")
            return {"url": url, "error": str(e)}


class JinaAPI:
    def __init__(self, api_token: str):
        self.base_url = "https://r.jina.ai"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
        }

    async def scrape_url(self, session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
        try:
            async with session.get(f"{self.base_url}/{url}", headers=self.headers) as response:
                response.raise_for_status()
                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    data = await response.json()
                else:
                    data = await response.text()
                print(f"Successfully scraped with Jina: {url}")
                return {"url": url, "data": data, "error": None}
        except aiohttp.ClientError as e:
            error_message = str(e)
            print(f"Error occurred while scraping with Jina {url}: {error_message}")
            return {"url": url, "data": None, "error": error_message}


class URLScraper:
    def __init__(self, output_file: str, use_jina: bool = False):
        self.firecrawl_api = FirecrawlAPI(settings.FIRECRAWL_API_KEY)
        self.jina_api = JinaAPI(settings.JINA_API_TOKEN)
        self.use_jina = use_jina
        self.firecrawl_rate_limit = settings.FIRECRAWL_RATE_LIMIT
        self.jina_rate_limit = settings.JINA_RATE_LIMIT
        self.last_request_time = 0
        self.output_file = output_file

    async def scrape_urls(self, urls: List[str]) -> AsyncIterator[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            for url in urls:
                await self._apply_rate_limit()

                if self.use_jina:
                    result = await self.jina_api.scrape_url(session, url)
                else:
                    result = await self.firecrawl_api.scrape_url(session, url)

                self.last_request_time = asyncio.get_event_loop().time()

                if "error" in result:
                    logger.error(f"Error scraping {result['url']}: {result['error']}")
                else:
                    logger.info(f"Successfully scraped: {result['url']}")

                yield result

    async def _apply_rate_limit(self) -> None:
        current_time = asyncio.get_event_loop().time()
        time_since_last_request = current_time - self.last_request_time
        rate_limit = self.jina_rate_limit if self.use_jina else self.firecrawl_rate_limit

        if time_since_last_request < 1 / rate_limit:
            await asyncio.sleep(1 / rate_limit - time_since_last_request)

    async def run(self, file_path: str) -> None:
        try:
            urls = FileHandler.load(file_path)
            async for result in self.scrape_urls(urls):
                FileHandler.append_jsonl(result, self.output_file)
                logger.info(f"Result for {result['url']} saved to {self.output_file}")
        except Exception as e:
            logger.exception(f"An error occurred: {str(e)}")

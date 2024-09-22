import asyncio
from rich.console import Console

from rmd.utils.scrape_urls import URLScraper
from rmd.core.config import file_paths, settings
from rmd.core.log import logger

console = Console()

def scrape_urls(
    url: str,
    output_file: str,
    use_jina: bool = settings.USE_JINA,
):
    """Scrape URLs from the input file."""

    if use_jina and not settings.JINA_API_TOKEN:
        console.print("[red]Error: JINA_API_TOKEN environment variable is not set.[/red]")
        raise

    async def run_scraper():
        scraper = URLScraper(output_file, use_jina)
        await scraper.run(url)

    asyncio.run(run_scraper())
    logger.debug(f"URLs scraped and saved to {output_file}")
    console.print(f"[green]URLs scraped and saved to {output_file}[/green]")
    return output_file


if __name__ == "__main__":
    # asyncio.run(links_main())
    # WebsiteToMarkdownConverter("https://typer.tiangolo.com/", file_paths.data_dir / "typer.md").convert()
    scrape_urls(url="https://typer.tiangolo.com/", output_file=file_paths.data_dir / "typer.md")

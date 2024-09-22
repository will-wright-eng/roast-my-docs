import os
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
import subprocess


@dataclass
class FilePaths:
    repo_root = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'],
                                                 universal_newlines=True).strip())
    data_dir: Path = repo_root / "data"
    log_file: Path = data_dir / "roast-my-docs.log"
    extracted_urls: Path = data_dir / "extracted_urls.jsonl"
    scraped_docs: Path = data_dir / "scraped_docs.jsonl"

    # @classmethod
    # def create(cls):
    #     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    #     return cls(
    #         extracted_urls=repo_root / f"data/{timestamp}_extracted_urls.jsonl",
    #         scraped_docs=repo_root / f"data/{timestamp}_scraped_docs.jsonl",
    #         # classified_md=repo_root / f"data/results/{timestamp}_classified_md.json",
    #         log_file=repo_root / "data/roast-my-docs.log",
    #         # analysis_results=repo_root / f"data/results/{timestamp}_analysis_results.md",
    #     )


@dataclass
class Settings:
    MAX_LINKS: int = 20
    USE_JINA: bool = False
    PROCESS_ALL: bool = True
    FIRECRAWL_RATE_LIMIT: float = 1 / 60  # 1 request per 60 seconds
    JINA_RATE_LIMIT: float = 200 / 60  # 200 requests per 60 seconds
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY")
    FIRECRAWL_API_KEY: str = os.environ.get("FIRECRAWL_API_KEY")
    JINA_API_TOKEN: str = os.environ.get("JINA_API_TOKEN")


settings = Settings()
file_paths = FilePaths()

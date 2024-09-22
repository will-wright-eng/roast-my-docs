import os
import json
from typing import Any, Dict, List


from rmd.core.log import logger


class FileHandler:
    @staticmethod
    def _ensure_directory(file_path: str):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    @staticmethod
    def _read_file(file_path: str, mode: str = "r", encoding: str = "utf-8"):
        with open(file_path, mode, encoding=encoding) as file:
            return file.read()

    @staticmethod
    def _write_file(data: Any, file_path: str, mode: str = "w"):
        FileHandler._ensure_directory(file_path)
        with open(file_path, mode, encoding='utf-8') as file:
            file.write(data)
        logger.info(f"Data {'saved to' if mode == 'w' else 'appended to'} {file_path}")

    @staticmethod
    def load(file_path: str) -> Any:
        _, ext = os.path.splitext(file_path)
        if ext == ".json":
            return FileHandler.load_json(file_path)
        elif ext == ".jsonl":
            return FileHandler.load_jsonl(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    @staticmethod
    def load_json(file_path: str) -> Dict[str, Any]:
        return json.loads(FileHandler._read_file(file_path))

    @staticmethod
    def load_jsonl(file_path: str) -> List[Dict[str, Any]]:
        return [json.loads(line) for line in FileHandler._read_file(file_path).splitlines()]

    @staticmethod
    def save_json(data: Any, file_path: str, indent: int = 4):
        FileHandler._write_file(json.dumps(data, indent=indent), file_path)

    @staticmethod
    def append_jsonl(item: Dict[str, Any], file_path: str):
        FileHandler._write_file(json.dumps(item) + "\n", file_path, mode="a")

    @staticmethod
    def save_markdown(data: str, file_path: str):
        FileHandler._write_file(data, file_path, mode="w")

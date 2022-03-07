import json
import pathlib
import re
import shutil
from typing import Dict

import requests

import src.utils
from src.errors import UserIdNotFoundError


class Downloader:
    def __init__(self, *, num_pages: int = 1) -> None:
        self.num_pages = num_pages
        self.headers = self._load_headers()

    def download(self) -> None:
        base_url = self._prepare_base_url()
        output_directory = self._prepare_output_directory()
        for page in range(1, self.num_pages + 1):
            output_file = output_directory.joinpath(f"page-{page}.html")
            print(f"Downloading '{output_file.name}'... ", end="", flush=True)
            response = requests.post(base_url.format(page=page), headers=self.headers)
            output_file.write_text(response.text)
            print("Done.")
            if page != self.num_pages:
                src.utils.sleep(5)

    def _get_user_id(self) -> str:
        user_id = re.search(r" uid=(\d+);", self.headers["cookie"])
        if user_id is None:
            raise UserIdNotFoundError()
        return user_id.groups()[0]

    def _load_headers(self) -> Dict[str, str]:
        with open("headers.json") as file:
            return json.load(file)

    def _prepare_base_url(self) -> str:
        user_id = self._get_user_id()
        base_url = f"https://www.kinopoisk.ru/user/{user_id}/votes/list/ord/date/page/"
        return base_url + "{page}/"

    @staticmethod
    def _prepare_output_directory() -> pathlib.Path:
        pages = pathlib.Path.cwd().joinpath("pages")
        if pages.is_dir():
            shutil.rmtree(pages)
        pages.mkdir()
        return pages

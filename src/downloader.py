import json
import pathlib
import re
import shutil
from typing import Dict

import requests

import src.utils
from src.errors import UserIdNotFoundError


class Downloader:
    def __init__(self) -> None:
        self._headers = self._load_headers()

    def download_vote_pages(self, *, num_pages: int) -> None:
        votes_url = self._prepare_votes_url()
        output_directory = self._prepare_output_directory("votes")
        for page in range(1, num_pages + 1):
            output_file = output_directory.joinpath(f"page-{page}.html")
            print(f"Downloading '{output_file.name}'... ", end="", flush=True)
            response = requests.post(votes_url.format(page=page), headers=self._headers)
            output_file.write_text(response.text)
            print("Done.")
            if page != num_pages:
                src.utils.sleep(5)

    def _get_user_id(self) -> str:
        user_id = re.search(r" uid=(\d+);", self._headers["cookie"])
        if user_id is None:
            raise UserIdNotFoundError()
        return user_id.groups()[0]

    def _load_headers(self) -> Dict[str, str]:
        with open("headers.json") as file:
            return json.load(file)

    @staticmethod
    def _prepare_output_directory(directory: str) -> pathlib.Path:
        output_path = pathlib.Path.cwd().joinpath(directory)
        if output_path.is_dir():
            shutil.rmtree(output_path)
        output_path.mkdir()
        return output_path

    def _prepare_votes_url(self) -> str:
        user_id = self._get_user_id()
        base_url = f"https://www.kinopoisk.ru/user/{user_id}/votes/list/ord/date/page/"
        return base_url + "{page}/"

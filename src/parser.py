import json
import pathlib
import re
from datetime import datetime
from typing import List, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag

from src.errors import (
    MovieUrlNotFoundError,
    RatingDateNotFoundError,
    RatingKpNotFoundError,
    RatingMyNotFoundError,
    TitleRuNotFoundError,
)
from src.movie import Movie


class Parser:
    def parse_vote_pages(self) -> None:
        today = datetime.now().strftime("%Y-%m-%d")
        output_file = f"votes-{today}.json"
        movies = [movie.dict() for movie in self._get_movies()]
        with open(output_file, "w") as file:
            json.dump(movies, file, ensure_ascii=False, indent=4, default=str)
            print(f"Dumped {len(movies)} movies to '{output_file}'.")

    @staticmethod
    def _get_movie_url(movie: Tag) -> str:
        a = movie.find("a")
        if not isinstance(a, Tag) or not a.has_attr("href"):
            raise MovieUrlNotFoundError()
        return f'https://www.kinopoisk.ru{a["href"]}'

    def _get_movies(self) -> List[Movie]:
        movies: List[Movie] = []
        for page in pathlib.Path.cwd().joinpath("votes").iterdir():
            soup = BeautifulSoup(page.read_text(), "lxml")
            movies.extend(
                [
                    Movie(
                        title_ru=self._get_title_ru(movie),
                        title_en=self._get_title_en(movie),
                        movie_url=self._get_movie_url(movie),
                        rating_kp=self._get_rating_kp(movie),
                        rating_my=self._get_rating_my(movie),
                        rating_date=self._get_rating_date(movie),
                    )
                    for movie in soup.find_all("div", class_=["item", "even"])
                    if isinstance(movie, Tag) and movie.find("script") is not None
                ]
            )
        return movies

    @staticmethod
    def _get_rating_date(movie: Tag) -> datetime:
        div = movie.find("div", class_="date")
        if not isinstance(div, Tag) or div.string is None:
            raise RatingDateNotFoundError()
        return datetime.strptime(div.string, "%d.%m.%Y, %H:%M")

    @staticmethod
    def _get_rating_kp(movie: Tag) -> str:
        div = movie.find("div", class_="rating")
        if not isinstance(div, Tag) or div.b is None:
            raise RatingKpNotFoundError()
        return str(div.b.string)

    @staticmethod
    def _get_rating_my(movie: Tag) -> Optional[str]:
        script = movie.find("script", string=re.compile(".*rating.*"))
        if not isinstance(script, Tag) or not isinstance(script.string, str):
            raise RatingMyNotFoundError()
        # Zero length (i.e., no rating) in `\d{0,2}` is for views (просмотры).
        match = re.search(r".*rating: '(\d{0,2})'", script.string)
        if match is None:
            raise RatingMyNotFoundError()
        return match.groups()[0] or None

    @staticmethod
    def _get_title_en(movie: Tag) -> Optional[str]:
        div = movie.find("div", class_="nameEng")
        if not isinstance(div, Tag):
            return None
        return str(div.string) if div.string != "\xa0" else None

    @staticmethod
    def _get_title_ru(movie: Tag) -> str:
        div = movie.find("div", class_="nameRus")
        if not isinstance(div, Tag) or div.a is None:
            raise TitleRuNotFoundError()
        return str(div.a.string)

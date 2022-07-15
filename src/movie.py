import dataclasses
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Movie:
    title_ru: str
    title_en: str | None
    movie_url: str
    rating_kp: str
    rating_my: str | None
    rating_date: datetime

    def dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)

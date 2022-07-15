import dataclasses
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Movie:
    title_ru: str
    title_en: Optional[str]
    movie_url: str
    rating_kp: str
    rating_my: Optional[str]
    rating_date: datetime

    def dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)

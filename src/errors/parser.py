class MovieParserError(Exception):
    pass


class MovieUrlNotFoundError(MovieParserError):
    def __init__(self) -> None:
        super().__init__("no movie url found while parsing html")


class RatingDateNotFoundError(MovieParserError):
    def __init__(self) -> None:
        super().__init__("no rating date found while parsing html")


class RatingKpNotFoundError(MovieParserError):
    def __init__(self) -> None:
        super().__init__("no kinopoisk rating found while parsing html")


class RatingMyNotFoundError(MovieParserError):
    def __init__(self) -> None:
        super().__init__("no user rating found while parsing html")


class TitleRuNotFoundError(MovieParserError):
    def __init__(self) -> None:
        super().__init__("no russian title found while parsing html")

class KinopoiskHeadersError(Exception):
    pass


class UserIdNotFoundError(KinopoiskHeadersError):
    def __init__(self) -> None:
        super().__init__("cannot find user id in kinopoisk headers")

from src.downloader import Downloader
from src.parser import Parser


def main() -> None:
    Downloader().download_vote_pages(num_pages=2)
    Parser().parse_vote_pages()


if __name__ == "__main__":
    main()

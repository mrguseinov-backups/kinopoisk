from src.downloader import Downloader
from src.parser import Parser


def main() -> None:
    Downloader(num_pages=2).download()
    Parser().parse()


if __name__ == "__main__":
    main()

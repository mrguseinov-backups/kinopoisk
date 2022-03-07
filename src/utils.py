import time


def sleep(seconds: int) -> None:
    for i in range(seconds, 0, -1):
        message = f" Sleeping {i} second(s)."
        print(message, end="\r")
        time.sleep(1)
        print(" " * len(message), end="\r")

import time


class Timer:

    def __init__(self, logger, title):

        self.logger = logger
        self.title = title

    def __enter__(self):

        self.start = time.perf_counter()

        self.logger.info(
            f"{self.title}..."
        )

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        elapsed = (
            time.perf_counter()
            - self.start
        )

        self.logger.info(
            f"{self.title} finished in {elapsed:.2f}s"
        )
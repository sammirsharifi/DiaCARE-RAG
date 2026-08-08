import logging
from pathlib import Path


_LOGGERS = {}


def get_logger(name: str = "ExplainableCKG") -> logging.Logger:

    if name in _LOGGERS:
        return _LOGGERS[name]

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
    )

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    file = logging.FileHandler(
        log_dir / "project.log",
        encoding="utf-8",
    )
    file.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(file)

    logger.propagate = False

    _LOGGERS[name] = logger

    return logger
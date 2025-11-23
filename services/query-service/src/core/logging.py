import logging
import sys


def init_logging(service_name: str):
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    if not root.handlers:
        root.addHandler(handler)

    logging.info(f"Logging initialized for {service_name}")

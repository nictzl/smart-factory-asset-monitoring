import logging
import sys

def init_logging(service_name: str = "processing-service") -> None:
    """
    Initialize structured logging with consistent formatting.
    This is shared across all services for observability.
    """

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    # prevent duplicates if imported multiple times
    if not root.handlers:
        root.addHandler(handler)

    logging.getLogger().info(f"Logging initialized for {service_name}")

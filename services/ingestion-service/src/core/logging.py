import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name
        }

        if hasattr(record, "trace_id"):
            log_data["trace_id"] = record.trace_id

        return json.dumps(log_data)

def init_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)

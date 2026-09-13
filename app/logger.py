import logging
from pathlib import Path

from app.config import PROJECT_ROOT


LOG_DIRECTORY = PROJECT_ROOT / "data" / "logs"
LOG_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)

LOG_FILE = LOG_DIRECTORY / "agent.log"


logger = logging.getLogger("enterprise_ai_agent")

logger.setLevel(logging.INFO)


if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
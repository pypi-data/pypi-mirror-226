__all__ = ["get_logger"]

from api_compose.core.logging.adapter import LoggerAdapter
from api_compose.core.utils.settings import GlobalSettings


def get_logger(
        name: str,
        overwrite=True,
) -> LoggerAdapter:
    log_file_path = GlobalSettings.get().LOG_FILE_PATH
    LOGGING_LEVEL = GlobalSettings.get().LOGGING_LEVEL
    return LoggerAdapter(name=name, log_file_path=log_file_path, overwrite=overwrite, logging_level=LOGGING_LEVEL)

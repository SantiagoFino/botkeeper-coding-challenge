from logger import logger


def process_in_logfile(message: str) -> None:
    """
    Documentation
    """
    logger.info(f"record: {message}")
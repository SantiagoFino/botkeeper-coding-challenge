from logger import logger

async def process_in_logfile(message: str) -> None:
    """
    Documentation
    """
    logger.info(f"record: {message}")
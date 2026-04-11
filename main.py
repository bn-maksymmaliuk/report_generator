import asyncio
import logging
from app.config.logger_setup import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

async def main():
    logger.info("Application started")

if __name__ == "__main__":
    asyncio.run(main())
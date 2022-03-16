import logging
import asyncio
from aiostream import stream

from services import urparts_scraper
from database import save_rows


async def main():
    logging.basicConfig(level=logging.INFO)

    chunck_size = 10

    parts_generator = urparts_scraper.get_all_parts()

    async for chunk in stream.chunks(parts_generator, chunck_size):
        for part_task in chunk:
            parts = await part_task
            save_rows(parts)


if __name__ == "__main__":
    asyncio.run(main())

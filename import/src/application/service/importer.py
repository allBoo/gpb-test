import logging
from shared.data.source import Reader, Writer

logger = logging.getLogger(__name__)


class Importer:

    def __init__(self, reader: Reader, writer: Writer) -> None:
        self.reader = reader
        self.writer = writer

    async def import_data(self) -> int:
        imported = 0
        try:
            async with self.writer:
                async for item in self.reader.read():
                    await self.writer.write(item, self._on_failure)
                    imported += 1
                    if imported % 1000 == 0:
                        logger.info(f"Processed {imported} items")
            logger.info(f"Imported {imported} items")
        except Exception as e:
            logger.error(f"Failed to import data: {e}")
            imported = 0
        finally:
            await self.writer.close()

        return imported

    @staticmethod
    def _on_failure(item):
        logger.error(f"Failed to save item {item}")

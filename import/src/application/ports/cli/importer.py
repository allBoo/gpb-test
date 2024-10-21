import enum
import logging
import typer
import asyncio

from application.container import ApplicationContainer
from config import settings

from application.service.factory import ServiceFactory

logger = logging.getLogger(__name__)

__all__ = ['register']


async def cleanup(container: ApplicationContainer) -> None:
    async with container.get_database().get_connection() as connection:
        storage_service = ServiceFactory.get_storage_service(connection)
        await storage_service.cleanup()


async def run_batch_import(container: ApplicationContainer, log_path: str, zipped: bool) -> None:
    async with container.get_database().get_connection() as connection:
        importer = ServiceFactory.get_import_service(connection, log_path, zipped=zipped)
        imported = await importer.import_data()
        if imported:
            logger.info(f'Imported {imported} records from {log_path}')
        else:
            logger.error('Failed to import data')


def run_import(
    log_path: str = typer.Option(
        None,
        "-f", "--file",
        help="Path to the maillog file",
    ),
    truncate: bool = typer.Option(
        False,
        "-t", "--truncate",
        help="Truncate the database before import",
    ),
    zipped: bool = typer.Option(
        False,
        "-z", "--zip",
        help="Log file is ZIP compressed",
    ),
    debug: bool = typer.Option(
        False,
        "-d", "--debug",
        help="Additional logging",
    )
) -> None:
    if debug:
        logging.root.setLevel(logging.DEBUG)

    container = ApplicationContainer(settings)
    loop = asyncio.get_event_loop()

    if truncate:
        logger.info('Truncating database')
        loop.run_until_complete(cleanup(container))

    logger.info(f'Importing data from {log_path}...')
    loop.run_until_complete(run_batch_import(container, log_path, zipped))


def register(app: typer.Typer) -> None:
    app.command(name="import")(run_import)

import asyncio
import logging

from temporalio.client import Client
from temporalio.worker import Worker

from fact_checking_system.config import get_settings
from fact_checking_system.logging import configure_logging
from fact_checking_system.workflows import WORKFLOWS

logger = logging.getLogger(__name__)


async def serve() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)
    client = await Client.connect(
        settings.temporal_host,
        namespace=settings.temporal_namespace,
    )
    worker = Worker(
        client,
        task_queue=settings.temporal_task_queue,
        workflows=WORKFLOWS,
    )
    logger.info("worker started on task queue %s", settings.temporal_task_queue)
    await worker.run()


def run() -> None:
    asyncio.run(serve())


if __name__ == "__main__":
    run()

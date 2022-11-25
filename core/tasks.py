import logging
from payment.celery_ import app
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)
logger.setLevel(logging.INFO)


@app.task
def test_task():
    logger.info("Test task finished!")

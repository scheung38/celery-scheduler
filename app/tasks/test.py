import celery


@celery.task()
def print_hello():
    logger = print_hello.get_logger()
    logger.info("Hello1")


@celery.task()
def get_message():
    logger = get_message.get_logger()
    logger.info("Tuesday")

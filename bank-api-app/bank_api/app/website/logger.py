import logging

INSTANCE = None


def get_logger():
    global INSTANCE
    if INSTANCE is None:
        logFormatter = logging.Formatter('%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s')
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        logger.addHandler(consoleHandler)
        INSTANCE = logger

    return INSTANCE

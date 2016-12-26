from mylogging import setup_logging
import logging

setup_logging()
#logger = logging.getLogger(__name__)
logger = logging.getLogger()

logger.debug('This is DEBUG log')
logger.info('This is INFO log')
logger.warning('This is WARNING log')
logger.error('This is ERROR log')
logger.critical('This is CRITICAL log')
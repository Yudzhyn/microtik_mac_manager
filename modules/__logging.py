# logging
import logging
# environment variables
from os import environ
from sys import stdout

# configs
from configs import LOGGING_PATH

logger = logging.getLogger()

logging.basicConfig(filename=LOGGING_PATH, level=logging.INFO,
                    format='%(asctime)s %(levelname)s'
                           ' %(message)s (%(module)s - %(funcName)s)',
                    datefmt='%d-%m %H:%M:%S')

if environ.get("DEBUG_ENV"):
    handler = logging.StreamHandler(stdout)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

logger.info("+---------------------------------------------------------+")

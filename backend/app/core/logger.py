import logging
from app.core.config import settings


# Initialize the logger
logging.basicConfig()
logger = logging.getLogger(__name__)


# Handle logging settings
if settings.LOGGING_ENABLED == True:
    logger.setLevel(settings.LOGGING_LEVEL.upper()) # Use .upper() to ensure the log level is in uppercase
else:
    logger.addHandler(logging.NullHandler()) # If logging is disabled, add a NullHandler to the logger
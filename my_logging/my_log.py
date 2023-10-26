from loguru import logger

logger.remove()
logger.add("quest.log", rotation="10 MB", retention="2 weeks")

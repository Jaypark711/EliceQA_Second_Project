import os
import logging
from datetime import datetime

def setupLogger(name, log_dir="reports/logs"):
    os.makedirs(log_dir, exist_ok=True)

    logFile = os.path.join(log_dir, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    fileHandler = logging.FileHandler(logFile, encoding='utf-8')
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fileHandler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(fileHandler)

    return logger

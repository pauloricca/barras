import logging

# Create a logger
logger = logging.getLogger('glitch_logger')
logger.setLevel(logging.INFO)

# Create a file handler and set the log file path
log_file = 'log.log'
file_handler = logging.FileHandler(log_file)

# Create a formatter and set the format of the log messages
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

def log(*messages):
    logger.info(' '.join(str(msg) for msg in messages))

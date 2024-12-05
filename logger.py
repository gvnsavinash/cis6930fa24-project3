import logging
import os

def setup_logger(log_filename):
    """
    Sets up the logger configuration and returns a logger instance.
    
    Args:
        log_filename (str): The name of the log file where the logs will be written.
    
    Returns:
        logging.Logger: A logger instance configured to write logs to the specified file.
    """
    # Assuming the resources folder already exists
    abs_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file_path = os.path.join(abs_path, "resources", log_filename)
    
    # Create and configure the logger
    logger = logging.getLogger(log_filename)
    
    # Prevent duplicate logs
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # File handler for logging to file
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(logging.DEBUG)

        # Create a logging format
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the handlers to the logger
        logger.addHandler(file_handler)
    
    return logger

def log_message(logger, level, message):
    """
    Logs a message to the provided logger instance.
    
    Args:
        logger (logging.Logger): The logger instance to log messages.
        level (str): The level of the log ('info', 'debug', 'error').
        message (str): The message to log.
    """
    if level == 'info':
        logger.info(message)
    elif level == 'debug':
        logger.debug(message)
    elif level == 'error':
        logger.error(message)
    else:
        logger.warning(f"Unknown log level: {level}. Message: {message}")

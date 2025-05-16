import logging

# Configure the logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("trade_simulator.log"),
        logging.StreamHandler()
    ]
)

def get_logger(name):
    """Get a logger with the specified name."""
    return logging.getLogger(name)
import logging
from termcolor import colored

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'WARNING': 'yellow',
        'INFO': 'green',
        'DEBUG': 'blue',
        'CRITICAL': 'red',
        'ERROR': 'red',
    }

    def format(self, record):
        log_message = super().format(record)
        return colored(log_message, self.COLORS.get(record.levelname))

AGENT_LOGGER = logging.getLogger('agent_logger')
AGENT_LOGGER.setLevel(logging.DEBUG)

# Create a console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create a formatter
formatter = ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s')

# Set the formatter for the console handler
ch.setFormatter(formatter)

# Add the console handler to the logger
AGENT_LOGGER.addHandler(ch)
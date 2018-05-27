import logging
import os
from time import gmtime, strftime

from .version import __version__


app_data_path = 'log'
LOG_FOLDER = os.mkdir(app_data_path) if not os.path.exists(app_data_path) else None

logger = logging.getLogger('ipx_logger')

log_formatter = logging.Formatter('%(message)s')
log_file = 'runner_log_{}.txt'.format(strftime("%Y_%m_%d_%H_%M_%S", gmtime()))
log_file = os.path.join(os.getcwd(), app_data_path, log_file)

file_output = logging.FileHandler(log_file)
file_output.setFormatter(log_formatter)
file_output.setLevel(logging.INFO)
logger.addHandler(file_output)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(log_formatter)
logger.addHandler(console)

logger.setLevel(logging.INFO)

logger.info('runner version ' + __version__)
logger.info('Log file -> ' + log_file)

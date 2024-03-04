import logging
import os


logger = logging.getLogger("gameof15")
logger.setLevel(logging.DEBUG)

# Figured out how to do this by looking here: https://docs.python.org/3/library/logging.html#logging.basicConfig
#logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

# So I googled "set format for individual loggers python" and it took me to here: https://docs.python.org/3/howto/logging-cookbook.html#using-logging-in-multiple-modules

# To get milliseconds included: https://stackoverflow.com/a/7517430
formatter = logging.Formatter(fmt='%(asctime)s %(message)s', datefmt='%H:%M:%S')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# https://stackoverflow.com/questions/13733552/logger-configuration-to-log-to-file-and-print-to-stdout
file_handler = logging.FileHandler(os.path.splitext(os.path.split("gameof15")[1])[0] + ".log", mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

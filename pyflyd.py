
import argparse
import grp
import logging
import logging.handlers
import signal
import sys

import daemon
import lockfile

from src.communications_manager import SocketCommunicationsManager

import pyfly_init
import os

# Deafults
DATA_DIR = os.path.dirname(os.path.realpath(__file__)) # Script dir '/var/lib/pyfly'
LOG_FILENAME = "/tmp/pyfly.log"
LOG_LEVEL = logging.INFO

PY_FLY_GRP = 'pyfly'

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="Runs the PyFly Graph database.")
parser.add_argument("-l", "--log",
                    help="file to write log to (default '" + LOG_FILENAME + "')")
parser.add_argument("--data-dir", dest='data_dir',
                    help="data directory (default '" + DATA_DIR + "')")

# If the log file is specified on the command line then override the default
args = parser.parse_args()
if args.log:
    LOG_FILENAME = args.log
if args.data_dir:
    DATA_DIR = args.data_dir

#######################################################################
#                               LOGGING                               #
#######################################################################
# Configure logging to log to a file, making a new file at midnight
#  and keeping the last 3 day's data
# Give the logger a unique name (good practice)
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and
#  keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME,
                                                    when="midnight",
                                                    backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)


# Make a class we can use to capture stdout and sterr in the log
class MyLogger:
    def __init__(self, logger, level):
        """Needs a logger and a logger level."""
        self.logger = logger
        self.level = level

    def write(self, message):
        # Only log if there is a message (not just a new line)
        if message.rstrip() != "":
            self.logger.log(self.level, message.rstrip())

    def flush(self):
        pass


# Replace stdout with logging to file at INFO level
sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger(logger, logging.ERROR)

#######################################################################
#                               DAEMON                                #
#######################################################################
print('Starting ...')
context = daemon.DaemonContext(
    working_directory=DATA_DIR,
    umask=0o002,
    pidfile=lockfile.FileLock('/var/run/pyfly.pid'),
)

# TODO
context.signal_map = {
    signal.SIGTERM: exit, #program_cleanup,
    signal.SIGHUP: 'terminate',
    # signal.SIGUSR1: reload_program_config,
}

mail_gid = grp.getgrnam(PY_FLY_GRP).gr_gid
context.gid = mail_gid

# context.files_preserve = [important_file, interesting_file]

# initial_program_setup()

# run the daemon
with context:
    print('Running ...')
    pyfly_init.init()
    # SocketCommunicationsManager().run()

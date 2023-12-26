import logging
import os

class Logger():
    """A Logger based off of a session. Will append log data to end of logs associated with a specific session."""
    LOG_FOLDER = os.path.normcase(os.path.dirname(os.path.realpath(__file__))).replace("\\spiral\\utils", "\\logs")

    # Just to allow includes to be simpler.
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def __init__(self, session_key, log_level=logging.INFO):
        """Logger's log level is INFO by default."""
        self.update_session(log_level, session_key)
    
    def update_session(self, log_level, session_key=None):
        # Session Stuff
        if session_key:
            self.session_key = session_key
            self.log_file_name = self.session_key + '.log'
            self.path_to_file = Logger.LOG_FOLDER + '\\' + self.log_file_name

            # Logger Stuff
            self.logger = logging.getLogger(session_key)
            file_handler = logging.FileHandler(self.path_to_file)
            file_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter("[%(threadName)s] %(asctime)s: %(levelname)s: %(message)s")
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        self.logger.setLevel(log_level) # Loggers log level is set here!
    
    def write(self, message, log_level=logging.INFO):
        """Logs will only be written if log_level of message is equal to or higher than logger's log_level"""
        self.logger.log(log_level, message)

    def log_subprocess_output(self, output, log_level=logging.INFO):
        lines = output.split("\n")
        for line in lines:
            self.write(line.strip(), log_level)

# On import if log folder doesn't exist make it.
if not os.path.exists(Logger.LOG_FOLDER):
    print("Creating missing log folder: " + Logger.LOG_FOLDER)
    os.makedirs(Logger.LOG_FOLDER)
import os
from threading import Lock

class LogLevels:
    """A log with level 0 will"""
    TESTING = 0 # Logger will print every log, including 'testing' messages.
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    NECESSARY = 4 # Logger will print the least amount of logs. Only those that are necessary.

class Logger:
    """A Logger based off of a session. Will append log data to end of logs associated with a specific session."""
    LOG_FOLDER = os.path.normcase(os.path.dirname(os.path.realpath(__file__))) + "\\logs"
    _CURRENT_SESSIONS = {} # Map of all current sessions to a threading lock.

    def __init__(self, session_key, log_level=LogLevels.MEDIUM):
        self.update_session(session_key, log_level)
    
    def update_session(self, session_key, log_level):
        self.session_key = session_key
        self.log_level = log_level
        self.log_file_name = self.session_key + '.log'
        self.path_to_file = Logger.LOG_FOLDER + '\\' + self.log_file_name
        if self.session_key not in Logger._CURRENT_SESSIONS:
            Logger._CURRENT_SESSIONS[self.session_key] = Lock()
    
    def write(self, text, log_level=LogLevels.MEDIUM):
        """Logs will only be written if log_level of message is equal to or higher than logger's log_level"""
        if log_level < self.log_level:
            return

        with Logger._CURRENT_SESSIONS[self.session_key]:
            with open(self.path_to_file, 'a') as file:
                file.write(text)

    def __enter__(self):
        """This method is preferred when you want to ignore log_levels."""
        Logger._CURRENT_SESSIONS[self.session_key].acquire()
        self.file = open(self.path_to_file, 'a')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        Logger._CURRENT_SESSIONS[self.session_key].release()

# On import if log folder doesn't exist make it.
if not os.path.exists(Logger.LOG_FOLDER):
    print("Attempting to create missing log folder: " + Logger.LOG_FOLDER)
    os.makedirs(Logger.LOG_FOLDER)

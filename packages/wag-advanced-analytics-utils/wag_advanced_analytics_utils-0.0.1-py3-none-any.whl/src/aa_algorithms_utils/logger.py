import json
import os
import sys

class Logger:
    """
    Logger object that logs important messages and prints them to the terminal/console.

    Attributes
    ----------

    Methods
    -------
    __init__(self):
    __repr__(self):
    error(cls, message, message_context = None):
    warn(cls, message, message_context = None):
    info(cls, message, message_context = None):
    debug(cls, message, message_context = None):
    __log(log_level, level, severity, message, message_context):
    dd(string):
    """

    def __repr__(self):
        return "Logging class"

    @classmethod
    def error(
        cls, message, message_context=None
    ):
        """
        Log error message

        Parameters
        ----------
        message : str
            Message to log
        message_context : dict, optional
            ?

        Returns
        -------
        None
        """
        log_level = "error"
        level = 3
        severity = "ERROR"

        cls.__log(log_level, level, severity, message, message_context)

    @classmethod
    def warn(cls, message, message_context=None):
        """
        Log warning message

        Parameters
        ----------
        message : str
            Message to log
        message_context : dict, optional
            All the details we can pass into the dictionary, that we log.

        Returns
        -------
        None
        """
        log_level = "warn"
        level = 4
        severity = "WARNING"

        cls.__log(log_level, level, severity, message, message_context)

    @classmethod
    def info(cls, message, message_context=None):
        """
        Log info message

        Parameters
        ----------
        message : str
            Message to log
        message_context : dict, optional
            ?

        Returns
        -------
        None
        """
        log_level = "info"
        level = 6
        severity = "INFORMATION"

        cls.__log(log_level, level, severity, message, message_context)

    @classmethod
    def debug(cls, message, message_context=None):
        """
        Log debug message

        Parameters
        ----------
        message : str
            Message to log
        message_context : dict, optional
            All the details we can pass into the dictionary, that we log.

        Returns
        -------
        None
        """

        if os.environ["ENVIRONMENT"] == "production":
            return

        log_level = "debug"
        level = 8
        severity = "DEBUG"

        cls.__log(log_level, level, severity, message, message_context)

    @staticmethod
    def __log(
        log_level, level, severity, message, message_context
    ):
        """
        Collect log information and print it to the terminal/console.

        Parameters
        ----------
        log_level : str
            Sys log level.
        level : int
            Int that describes sys log level
        severity : str
            Log level all written out in caps.
        message : str
            Message to log
        message_context : dict
            All the details we can pass into the dictionary, that we log.

        Returns
        -------
        None
        """

        json_log_message = {
            "logLevel": log_level,
            "level": level,
            "severity": severity,
            "message": message,
            "wag_system": os.environ["WAG_SYSTEM"],
            "environment": os.environ["ENVIRONMENT"],
        }

        if message_context != None:
            for key in message_context:
                json_log_message[key] = message_context[key]

        print(json.dumps(json_log_message), flush=True)

    @staticmethod
    def dd(string):
        print(string)
        sys.exit()

# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 18.12.2023

  Purpose: base classes for logs subsystem.
"""

from inspect import currentframe
from queue import Queue
from threading import Thread

from jsktoolbox.attribtool import ReadOnlyClass
from jsktoolbox.raisetool import Raise
from jsktoolbox.libs.base_data import BData

from disco_libs.system import LogClient, LogProcessor


class _Keys(object, metaclass=ReadOnlyClass):
    """Keys container class.

    For internal use only.
    """

    LOGGER: str = "__logger_client__"
    LOG_PROCESSOR: str = "__engine__"
    LOG_QUEUE: str = "__logger_queue__"
    TH_LOGGER: str = "__th_logger__"


class BLogProcessor(BData):
    """BLogProcessor base class.

    Container for logger processor methods.
    """

    @property
    def th_log(self) -> Thread:
        """Give me thread logger handler."""
        if _Keys.TH_LOGGER not in self._data:
            self._data[_Keys.TH_LOGGER] = None
        return self._data[_Keys.TH_LOGGER]

    @th_log.setter
    def th_log(self, value: Thread) -> None:
        self._data[_Keys.TH_LOGGER] = value

    @property
    def qlog(self) -> Queue:
        """Give me access to queue handler."""
        if _Keys.LOG_QUEUE not in self._data:
            self._data[_Keys.LOG_QUEUE] = Queue()
        return self._data[_Keys.LOG_QUEUE]

    @qlog.setter
    def qlog(self, value: Queue) -> None:
        """Setter for logging queue."""
        if not isinstance(value, Queue):
            raise Raise.error(
                f"Expected Queue type, received: '{type(value)}'",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.LOG_QUEUE] = value

    @property
    def log_processor(self) -> LogProcessor:
        """Give me handler for log processor."""
        if _Keys.LOG_PROCESSOR not in self._data:
            self._data[_Keys.LOG_PROCESSOR] = None
        return self._data[_Keys.LOG_PROCESSOR]

    @log_processor.setter
    def log_processor(self, value: LogProcessor) -> None:
        """Setter for log processor instance."""
        self._data[_Keys.LOG_PROCESSOR] = value


class BLogClient(BData):
    """BLogClass base class.

    Container for logger methods.
    """

    @property
    def logger(self) -> LogClient:
        """Give me logger handler."""
        if _Keys.LOGGER not in self._data:
            self._data[_Keys.LOGGER] = None
        return self._data[_Keys.LOGGER]

    @logger.setter
    def logger(self, arg: LogClient) -> None:
        """Set logger instance."""
        self._data[_Keys.LOGGER] = arg


# #[EOF]#######################################################################

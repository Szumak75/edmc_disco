# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 18.12.2023

  Purpose: main class
"""

from inspect import currentframe
from threading import Thread
from queue import Queue

from disco.jsktoolbox.raisetool import Raise
from disco.jsktoolbox.edmctool.base import BLogClient, BLogProcessor
from disco.jsktoolbox.edmctool.logs import LogClient, LogProcessor

from disco.data import DiscoData
from disco.database import Database, DBProcessor


class Disco(BLogProcessor, BLogClient):
    """Main class."""

    def __init__(self) -> None:
        """Constructor."""

        # data
        self.data.plugin_name = "EDDisco"
        self.data.version = "1.1.2"

        # database
        self.data.db_processor = DBProcessor(Database(False).session)

        # logging subsystem
        self.qlog = Queue()
        self.log_processor = LogProcessor(self.data.plugin_name)
        self.logger = LogClient(self.qlog)

        # logging thread
        self.th_log = Thread(
            target=self.th_logger, name=f"{self.data.plugin_name} log worker"
        )

        if self.th_log:
            self.th_log.daemon = True
            self.th_log.start()

        if self.logger:
            self.logger.debug = f"{self.data.plugin_name} object creation complete."

    @property
    def data(self) -> DiscoData:
        """Return data access."""
        if self._get_data(key="disco", default_value=None) is None:
            self._set_data(key="disco", value=DiscoData(), set_default_type=DiscoData)
        return self._get_data(key="disco")  # type: ignore

    @data.setter
    def data(self, value: DiscoData) -> None:
        self._set_data(key="disco", value=value, set_default_type=DiscoData)

    def th_logger(self) -> None:
        """Def th_logger - thread logs processor."""
        if self.logger:
            self.logger.info = "Starting logger worker"
        while not self.data.shutting_down:
            while True:
                log = self.qlog.get(True)
                if log is None:
                    break
                if self.log_processor:
                    self.log_processor.send(log)


# #[EOF]#######################################################################

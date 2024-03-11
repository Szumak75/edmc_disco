# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 18.12.2023

  Purpose: main class
"""

from inspect import currentframe
from threading import Thread

from jsktoolbox.raisetool import Raise


from disco_libs.data import DiscoData
from disco_libs.database import Database, DBProcessor

from disco_libs.base_logs import BLogClient, BLogProcessor
from disco_libs.system import LogClient, LogProcessor


class Disco(BLogProcessor, BLogClient):
    """Main class."""

    def __init__(self) -> None:
        """Constructor."""

        # data
        self.data.pluginname = "EDDisco"
        self.data.version = "1.0.3-dev"

        # database
        self.data.db_processor = DBProcessor(Database(False).session)

        # logging subsystem
        # self.qlog = Queue()
        self.log_processor = LogProcessor(self.data.pluginname)
        self.logger = LogClient(self.qlog)

        # logging thread
        self.thlog = Thread(
            target=self.th_logger, name=f"{self.data.pluginname} log worker"
        )

        if self.thlog:
            self.thlog.daemon = True
            self.thlog.start()

        if self.logger:
            self.logger.debug = f"{self.data.pluginname} object creation complete."

    @property
    def data(self) -> DiscoData:
        """Give me data access."""
        if "disco" not in self._data:
            self._data["disco"] = DiscoData()
        return self._data["disco"]

    @data.setter
    def data(self, value: DiscoData) -> None:
        if isinstance(value, DiscoData):
            self._data["disco"] = value
        else:
            raise Raise.error(
                f"Expected DiscoData type, received: '{type(value)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )

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

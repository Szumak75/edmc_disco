# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 18.12.2023

  Purpose: data container classes.
"""

from inspect import currentframe
from typing import Optional, Union

from disco.jsktoolbox.attribtool import ReadOnlyClass
from disco.jsktoolbox.basetool.data import BData
from disco.jsktoolbox.raisetool import Raise
from disco.jsktoolbox.edmctool.stars import StarsSystem

from disco.database import DBProcessor
from disco.db_models.system import TSystem


class _Keys(object, metaclass=ReadOnlyClass):
    """Keys container class."""

    CMDR: str = "cmdr"
    DIALOG: str = "dialog"
    JUMP_RANGE: str = "jump_range"
    PLUGIN_NAME: str = "pluginname"
    PROCESSOR: str = "processor"
    SHUTDOWN: str = "shutdown"
    STARS_SYSTEM: str = "stars_system"
    SYSTEM: str = "system"
    VERSION: str = "version"


class SimpleData(BData):
    """SimpleData container."""

    def __init__(self) -> None:
        """Initialize dataset."""
        self._data[_Keys.CMDR] = ""
        self._data[_Keys.PLUGIN_NAME] = ""
        self._data[_Keys.VERSION] = ""
        self._data[_Keys.SHUTDOWN] = False

    @property
    def plugin_name(self) -> str:
        """Give me pluginname."""
        return self._data[_Keys.PLUGIN_NAME]

    @plugin_name.setter
    def plugin_name(self, value: str) -> None:
        if value is not None and isinstance(value, str):
            self._data[_Keys.PLUGIN_NAME] = value

    @property
    def version(self) -> str:
        """Give me version."""
        return self._data[_Keys.VERSION]

    @version.setter
    def version(self, value: str) -> None:
        if value is not None and isinstance(value, str):
            self._data[_Keys.VERSION] = value

    @property
    def cmdr(self) -> str:
        """Give me commander name."""
        return self._data[_Keys.CMDR]

    @cmdr.setter
    def cmdr(self, value: str) -> None:
        if value is not None and value != self.cmdr:
            self._data[_Keys.CMDR] = value

    @property
    def shutting_down(self) -> bool:
        """Give me access to shutting_down flag."""
        return self._data[_Keys.SHUTDOWN]

    @shutting_down.setter
    def shutting_down(self, value: bool) -> None:
        if isinstance(value, bool):
            self._data[_Keys.SHUTDOWN] = value
        else:
            raise Raise.error(
                f"Expected boolean type, received: '{type(value)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )


class DiscoData(SimpleData):
    """Data container for Disco dialogs dataset."""

    def __init__(self) -> None:
        """Initialize dataset."""
        SimpleData.__init__(self)
        self._data[_Keys.SYSTEM] = None
        self._data[_Keys.PROCESSOR] = None
        self._data[_Keys.DIALOG] = None

    @property
    def db_processor(self) -> DBProcessor:
        """Database processor."""
        return self._data[_Keys.PROCESSOR]

    @db_processor.setter
    def db_processor(self, value: DBProcessor) -> None:
        self._data[_Keys.PROCESSOR] = value

    @property
    def dialog(self) -> object:
        """Return optional DiscoMainDialog object."""
        return self._data[_Keys.DIALOG]

    @dialog.setter
    def dialog(self, value: object) -> None:
        """Set DiscoMainDialog object."""
        self._data[_Keys.DIALOG] = value

    @property
    def system(self) -> TSystem:
        """TSystem dataset."""
        if self._data[_Keys.SYSTEM] is None:
            return None  # type: ignore
        out: TSystem = self._data[_Keys.SYSTEM]
        return out

    @system.setter
    def system(self, value: TSystem) -> None:
        if value is None:
            return
        if isinstance(value, TSystem):
            self._data[_Keys.SYSTEM] = value
        else:
            raise Raise.error(
                f"Expected TSystem type, received: '{type(value)}'",
                TypeError,
                self._c_name,
                currentframe(),
            )


class RscanData(SimpleData):
    """Data container for username and current system."""

    def __init__(self) -> None:
        """Initialize dataset."""
        SimpleData.__init__(self)
        self._data[_Keys.JUMP_RANGE] = None
        self._data[_Keys.STARS_SYSTEM] = StarsSystem()

    def __repr__(self) -> str:
        """Give me class dump."""
        return (
            f"{self._c_name}(cmdr='{self._data[_Keys.CMDR]}', "
            f"plugin_name='{self._data[_Keys.PLUGIN_NAME]}', "
            f"version='{self._data[_Keys.VERSION]}', "
            f"jump_range={self._data[_Keys.JUMP_RANGE]}, "
            f"{self._data[_Keys.STARS_SYSTEM]})"
        )

    @property
    def star_system(self) -> StarsSystem:
        """Give me StarsSystem object."""
        return self._data[_Keys.STARS_SYSTEM]

    @star_system.setter
    def star_system(self, value: StarsSystem) -> None:
        if value is None:
            self._data[_Keys.STARS_SYSTEM] = StarsSystem()
        elif isinstance(value, StarsSystem):
            self._data[_Keys.STARS_SYSTEM] = value

    @property
    def jump_range(self) -> Optional[float]:
        """Give me jump range."""
        return self._data[_Keys.JUMP_RANGE]

    @jump_range.setter
    def jump_range(self, value: Union[str, int, float]) -> None:
        if value is not None and isinstance(value, (str, int, float)):
            try:
                self._data[_Keys.JUMP_RANGE] = float(value)
            except Exception:
                pass


# #[EOF]#######################################################################

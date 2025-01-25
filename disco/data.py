# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 18.12.2023

  Purpose: data container classes.
"""

from typing import Optional

from disco.jsktoolbox.attribtool import ReadOnlyClass
from disco.jsktoolbox.basetool.data import BData

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
        self._set_data(key=_Keys.CMDR, value="", set_default_type=str)
        self._set_data(key=_Keys.PLUGIN_NAME, value="", set_default_type=str)
        self._set_data(key=_Keys.VERSION, value="", set_default_type=str)
        self._set_data(key=_Keys.SHUTDOWN, value=False, set_default_type=bool)

    @property
    def plugin_name(self) -> str:
        """Return plugin name."""
        return self._get_data(key=_Keys.PLUGIN_NAME)  # type: ignore

    @plugin_name.setter
    def plugin_name(self, value: str) -> None:
        """Set plugin name."""
        self._set_data(
            key=_Keys.PLUGIN_NAME,
            value=value,
        )

    @property
    def version(self) -> str:
        """Return version string."""
        return self._get_data(
            key=_Keys.VERSION,
        )  # type: ignore

    @version.setter
    def version(self, value: str) -> None:
        """Set version string."""
        self._set_data(
            key=_Keys.VERSION,
            value=value,
        )

    @property
    def cmdr(self) -> str:
        """Return commander name."""
        return self._get_data(key=_Keys.CMDR)  # type: ignore

    @cmdr.setter
    def cmdr(self, value: str) -> None:
        """Set commander name."""
        self._set_data(
            key=_Keys.CMDR,
            value=value,
        )

    @property
    def shutting_down(self) -> bool:
        """Return shutting_down flag."""
        return self._get_data(key=_Keys.SHUTDOWN)  # type: ignore

    @shutting_down.setter
    def shutting_down(self, value: bool) -> None:
        """Set shutting_down flag."""
        self._set_data(
            key=_Keys.SHUTDOWN,
            value=value,
        )


class DiscoData(SimpleData):
    """Data container for Disco dialogs dataset."""

    def __init__(self) -> None:
        """Initialize dataset."""
        SimpleData.__init__(self)
        self._set_data(key=_Keys.SYSTEM, value=None, set_default_type=Optional[TSystem])
        self._set_data(
            key=_Keys.PROCESSOR, value=None, set_default_type=Optional[DBProcessor]
        )
        self._set_data(
            key=_Keys.DIALOG,
            value=None,
            set_default_type=Optional[object]
        )

    @property
    def db_processor(self) -> DBProcessor:
        """Database processor."""
        return self._get_data(
            key=_Keys.PROCESSOR,
        )  # type: ignore

    @db_processor.setter
    def db_processor(self, value: DBProcessor) -> None:
        """Set database processor."""
        self._set_data(
            key=_Keys.PROCESSOR,
            value=value,
        )

    @property
    def dialog(self) -> object:
        """Return optional DiscoMainDialog object."""
        return self._get_data(
            key=_Keys.DIALOG,
        )

    @dialog.setter
    def dialog(self, value: object) -> None:
        """Set DiscoMainDialog object."""
        self._set_data(
            key=_Keys.DIALOG,
            value=value,
        )

    @property
    def system(self) -> TSystem:
        """TSystem dataset."""
        return self._get_data(
            key=_Keys.SYSTEM,
        )  # type: ignore

    @system.setter
    def system(self, value: TSystem) -> None:
        """Set TSystem dataset."""
        self._set_data(
            key=_Keys.SYSTEM,
            value=value,
        )


# #[EOF]#######################################################################

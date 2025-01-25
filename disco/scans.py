# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 16.03.2023

  Purpose: For discovered data analyze.
"""

from inspect import currentframe
from typing import List
from disco.jsktoolbox.attribtool import ReadOnlyClass
from disco.jsktoolbox.raisetool import Raise
from disco.jsktoolbox.basetool.data import BData

from disco.db_models import (
    TBody,
    TBodyFeatures,
    TBodyGenuses,
    TGenus,
    # TGenusScan,
    TBodySignals,
    TSignal,
    TCodex,
    TBodyCodexes,
)


class _Keys(object, metaclass=ReadOnlyClass):
    """Keys container class."""

    BODY: str = "body"


class ScansAnalysis(BData):
    """ScansAnalysis class.

    Analyzes discoveries in the system.
    """

    def __init__(self, body: TBody) -> None:
        """Constructor."""

        if not isinstance(body, TBody):
            raise Raise.error(
                f"Expected TBody type, received: '{type(body)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._set_data(key=_Keys.BODY, value=body, set_default_type=TBody)

    @property
    def body(self) -> TBody:
        """Return TBody object."""
        return self._get_data(key=_Keys.BODY)  # type: ignore

    @property
    def features(self) -> TBodyFeatures:
        """Return TBodyFeatures object."""
        return self.body.features

    @property
    def _genuses(self) -> List[TGenus]:
        """Return TBodyGenuses List."""
        item: TBodyGenuses = self.body.genuses
        return item.genuses

    @property
    def _signals(self) -> List[TSignal]:
        """Return TBodySignals List."""
        item: TBodySignals = self._data[_Keys.BODY].signals
        return item.signals

    @property
    def _codexes(self) -> List[TCodex]:
        """Return TBodyCodexes List."""
        item: TBodyCodexes = self.body.codexes
        return item.codexes


# #[EOF]#######################################################################

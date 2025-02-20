# -*- coding: UTF-8 -*-
"""
Created on 30 jan 2023.

@author: szumak@virthost.pl
"""

from typing import List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from disco.jsktoolbox.edmctool.ed_keys import EDKeys
from disco.db_models.base import DiscoBase


class TSignal(DiscoBase):
    """Table of Signals."""

    __tablename__: str = "signals"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    body_signals_id: Mapped[int] = mapped_column(ForeignKey("body_signals.id"))
    type: Mapped[str] = mapped_column(String)
    type_localised: Mapped[str] = mapped_column(String, nullable=True, default=None)
    count: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self) -> str:
        """Return string object."""
        return (
            f"TSignal(id='{self.id}', "
            f"body_signals_id='{self.body_signals_id}', "
            f"type='{self.type}', "
            f"type_localised='{self.type_localised}' "
            f"count='{self.count}' "
            ")"
        )


class TBodySignals(DiscoBase):
    """Table of Body Signals."""

    __tablename__: str = "body_signals"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    body_id: Mapped[int] = mapped_column(ForeignKey("bodies.id"))
    signals: Mapped[List["TSignal"]] = relationship("TSignal")

    def __repr__(self) -> str:
        """Return string object."""
        return (
            f"TBodySignals(id='{self.id}', "
            f"body_id='{self.body_id}', "
            f"signals='{self.signals}' "
            ")"
        )

    def event_parser(self, entry: dict) -> bool:
        """Event parser.

        Analyze dict from journal and import data into the object.
        """
        ret = False
        if EDKeys.SIGNALS in entry and entry[EDKeys.SIGNALS]:
            for e_signal in entry[EDKeys.SIGNALS]:
                test = False
                for item in self.signals:
                    if item.type == e_signal[EDKeys.TYPE]:
                        test = True
                        if item.count != e_signal[EDKeys.COUNT]:
                            item.count = e_signal[EDKeys.COUNT]
                            ret = True
                if not test:
                    signal = TSignal()
                    signal.type = e_signal[EDKeys.TYPE]
                    if EDKeys.TYPE_LOCALISED in e_signal:
                        signal.type_localised = e_signal[EDKeys.TYPE_LOCALISED]
                    signal.count = e_signal[EDKeys.COUNT]
                    self.signals.append(signal)
                    ret = True
        return ret

    def __count_type_signals(self, signal_type: str) -> int:
        """Return number of type signals."""
        count: int = 0
        for signal in self.signals:
            if signal.type_localised == signal_type:
                count = signal.count
                break
        return count

    @property
    def count_bio_signals(self) -> int:
        """Return number of biological signals if any."""
        return self.__count_type_signals("Biological")

    @property
    def count_geo_signals(self) -> int:
        """Return number of geological signals if any."""
        return self.__count_type_signals("Geological")

    @property
    def count_humans_signals(self) -> int:
        """Return number of humans signals if any."""
        return self.__count_type_signals("Human")


# #[EOF]#######################################################################

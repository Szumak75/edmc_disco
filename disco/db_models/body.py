# -*- coding: UTF-8 -*-
"""
Created on 30 jan 2023.

@author: szumak@virthost.pl
"""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from disco.jsktoolbox.edmctool.ed_keys import EDKeys

from disco.db_models.base import DiscoBase
from disco.db_models.body_features import TBodyFeatures
from disco.db_models.genuses import TBodyGenuses
from disco.db_models.signals import TBodySignals
from disco.db_models.codex import TBodyCodexes


class TBody(DiscoBase):
    """Table of Bodies."""

    __tablename__: str = "bodies"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String, default="")
    bodyid: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    parentid: Mapped[int] = mapped_column(
        Integer, index=True, nullable=False, default=0
    )
    system_id: Mapped[int] = mapped_column(ForeignKey("systems.id"))
    features: Mapped["TBodyFeatures"] = relationship("TBodyFeatures")
    signals: Mapped["TBodySignals"] = relationship("TBodySignals")
    genuses: Mapped["TBodyGenuses"] = relationship("TBodyGenuses")
    codexes: Mapped["TBodyCodexes"] = relationship("TBodyCodexes")

    def __init__(self) -> None:
        """Initialize object."""
        DiscoBase.__init__(self)
        self.features = TBodyFeatures()
        self.signals = TBodySignals()
        self.genuses = TBodyGenuses()
        self.codexes = TBodyCodexes()

    def __repr__(self) -> str:
        """Return string object."""
        return (
            f"TBody(id='{self.id}', "
            f"system_id='{self.system_id}', "
            f"parentid='{self.parentid}', "
            f"bodyid='{self.bodyid}', "
            f"name='{self.name}', "
            f"features='{self.features or ''}', "
            f"signals='{self.signals or ''}', "
            f"genuses='{self.genuses or ''}', "
            f"codexes='{self.codexes or ''}' "
            f")"
        )

    def event_parser(self, entry: dict) -> None:
        """Event parser.

        Analyze dict from journal and import data into the object.
        """
        if EDKeys.BODY in entry and entry[EDKeys.BODY] != self.name:
            self.name = entry[EDKeys.BODY]
        if EDKeys.BODY_NAME in entry and entry[EDKeys.BODY_NAME] != self.name:
            self.name = entry[EDKeys.BODY_NAME]
        if EDKeys.BODY_ID in entry and entry[EDKeys.BODY_ID] != self.bodyid:
            self.bodyid = entry[EDKeys.BODY_ID]
        if EDKeys.PARENTS in entry:
            if entry[EDKeys.PARENTS]:
                if self.parentid != list(entry[EDKeys.PARENTS][0].values())[0]:
                    self.parentid = list(entry[EDKeys.PARENTS][0].values())[0]


# #[EOF]#######################################################################

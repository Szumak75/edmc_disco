# -*- coding: UTF-8 -*-
"""
Created on 30 jan 2023.

@author: szumak@virthost.pl
"""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from disco_libs.db_models.base import Base
from disco_libs.db_models.body_features import TBodyFeatures
from disco_libs.db_models.genuses import TBodyGenuses
from disco_libs.db_models.signals import TBodySignals
from disco_libs.db_models.codex import TBodyCodexes


class TBody(Base):
    """Table of Bodies."""

    __tablename__ = 'bodies'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String, default='')
    bodyid: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    parentid: Mapped[int] = mapped_column(
        Integer, index=True, nullable=False, default=0
    )
    system_id: Mapped[int] = mapped_column(ForeignKey("systems.id"))
    features: Mapped["TBodyFeatures"] = relationship("TBodyFeatures")
    signals: Mapped["TBodySignals"] = relationship("TBodySignals")
    genuses: Mapped["TBodyGenuses"] = relationship("TBodyGenuses")
    codexes: Mapped["TBodyCodexes"] = relationship("TBodyCodexes")

    def __init__(self):
        """Initialize object."""
        Base.__init__(self)
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
        if 'Body' in entry and entry['Body'] != self.name:
            self.name = entry['Body']
        if 'BodyName' in entry and entry['BodyName'] != self.name:
            self.name = entry['BodyName']
        if 'BodyID' in entry and entry['BodyID'] != self.bodyid:
            self.bodyid = entry['BodyID']
        if 'Parents' in entry:
            if entry['Parents']:
                if self.parentid != list(entry['Parents'][0].values())[0]:
                    self.parentid = list(entry['Parents'][0].values())[0]


# #[EOF]#######################################################################

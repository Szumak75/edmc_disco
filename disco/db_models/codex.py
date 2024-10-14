# -*- coding: UTF-8 -*-
"""
Created on 30 jan 2023.

@author: szumak@virthost.pl
"""

from typing import List, Dict

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from disco.jsktoolbox.edmctool.ed_keys import EDKeys
from disco.db_models.base import DiscoBase


class TCodex(DiscoBase):
    """Table of Codex."""

    __tablename__: str = "codex"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    body_codexes_id: Mapped[int] = mapped_column(ForeignKey("body_codexes.id"))
    name: Mapped[str] = mapped_column(String)
    name_localised: Mapped[str] = mapped_column(String)
    subcategory: Mapped[str] = mapped_column(String)
    subcategory_localised: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    category_localised: Mapped[str] = mapped_column(String)
    latitude: Mapped[float] = mapped_column(
        Float(precision=6), nullable=True, default=None
    )
    longitude: Mapped[float] = mapped_column(
        Float(precision=6), nullable=True, default=None
    )

    def __repr__(self) -> str:
        """Return string object."""
        return (
            f"TCodex(id='{self.id}', "
            f"body_codexes_id='{self.body_codexes_id}', "
            f"name='{self.name}', "
            f"name_localised='{self.name_localised}', "
            f"subcategory='{self.subcategory}', "
            f"subcategory_localised='{self.subcategory_localised}', "
            f"category='{self.category}', "
            f"category_localised='{self.category_localised}', "
            f"latitude='{self.latitude or ''}', "
            f"longitude='{self.longitude or ''}' "
            ")"
        )


class TBodyCodexes(DiscoBase):
    """Table of Body Codexes."""

    __tablename__: str = "body_codexes"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    body_id: Mapped[int] = mapped_column(ForeignKey("bodies.id"))
    codexes: Mapped[List["TCodex"]] = relationship("TCodex")

    def __repr__(self) -> str:
        """Return string object."""
        return (
            f"TBodyCodexes(id='{self.id}', "
            f"body_id='{self.body_id}', "
            f"codexes='{self.codexes}' "
            ")"
        )

    def event_parser(self, entry: Dict) -> bool:
        """Event parser.

        Analyze dict from journal and import data into the object.
        """
        ret = False
        if entry[EDKeys.EVENT] == EDKeys.CODEX_ENTRY:
            test = False
            for item in self.codexes:
                if (
                    item.name == entry[EDKeys.NAME]
                    and item.name_localised == entry[EDKeys.NAME_LOCALISED]
                ):
                    test = True
                    ret = True
            if not test:
                tmp = TCodex()
                tmp.name = entry[EDKeys.NAME]
                tmp.name_localised = entry[EDKeys.NAME_LOCALISED]
                tmp.category = entry[EDKeys.CATEGORY]
                tmp.category_localised = entry[EDKeys.CATEGORY_LOCALISED]
                tmp.subcategory = entry[EDKeys.SUB_CATEGORY]
                tmp.subcategory_localised = entry[EDKeys.SUB_CATEGORY_LOCALISED]
                if EDKeys.LATITUDE in entry:
                    tmp.latitude = entry[EDKeys.LATITUDE]
                if EDKeys.LONGITUDE in entry:
                    tmp.longitude = entry[EDKeys.LONGITUDE]
                self.codexes.append(tmp)
                ret = True

        return ret


# #[EOF]#######################################################################

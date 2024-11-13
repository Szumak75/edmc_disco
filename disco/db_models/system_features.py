# -*- coding: UTF-8 -*-
"""
Created on 30 jan 2023.

@author: szumak@virthost.pl
"""

from typing import Optional

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from disco.jsktoolbox.edmctool.ed_keys import EDKeys
from disco.db_models.base import DiscoBase


class TSystemFeatures(DiscoBase):
    """Table of System Features."""

    __tablename__: str = "system_features"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    system_id: Mapped[int] = mapped_column(ForeignKey("systems.id"))
    _allegiance: Mapped[str] = mapped_column(String, nullable=False, default="")
    _security: Mapped[str] = mapped_column(String, nullable=False, default="")
    _population: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    def __repr__(self) -> str:
        """Return string object."""
        return (
            f"TSystemFeatures(id='{self.id}', "
            f"system_id='{self.system_id}', "
            f"allegiance='{self.allegiance or ''}', "
            f"security='{self.security or ''}', "
            f"population='{self.population}' "
            f")"
        )

    def event_parser(self, entry: dict) -> None:
        """Event parser.

        Analyze dict from journal and import data into the object.
        """
        if EDKeys.SYSTEM_ALLEGIANCE in entry and entry[EDKeys.SYSTEM_ALLEGIANCE] != self.allegiance:
            self.allegiance = entry[EDKeys.SYSTEM_ALLEGIANCE]
        if (
            EDKeys.SYSTEM_SECURITY_LOCALISED in entry
            and entry[EDKeys.SYSTEM_SECURITY_LOCALISED] != self.security
        ):
            self.security = entry[EDKeys.SYSTEM_SECURITY_LOCALISED]
        if EDKeys.POPULATION in entry and entry[EDKeys.POPULATION] != self.population:
            self.population = entry[EDKeys.POPULATION]

    @hybrid_property
    def allegiance(self) -> Optional[str]:
        """Get allegiance feature."""
        return self._allegiance

    @allegiance.inplace.setter # type: ignore
    def _allegiance_setter(self, value: Optional[str]) -> None:
        if not value:
            value = ""
        if not self._allegiance:
            if value:
                self._allegiance = value
        elif self._allegiance != value:
            self._allegiance = value

    @hybrid_property
    def population(self) -> int:
        """Get security feature."""
        return self._population

    @population.inplace.setter # type: ignore
    def _population_setter(self, value: int) -> None:
        if not value:
            value = 0
        if self._population != value:
            self._population = value

    @hybrid_property
    def security(self) -> Optional[str]:
        """Get security feature."""
        return self._security

    @security.inplace.setter # type: ignore
    def _security_setter(self, value: Optional[str]) -> None:
        if not value:
            value = ""
        if not self._security:
            if value:
                self._security = value
        elif self._security != value:
            self._security = value


# #[EOF]#######################################################################

# -*- coding: UTF-8 -*-
"""
Created on 30 jan 2023.

@author: szumak@virthost.pl
"""

from typing import Optional

from disco_libs.db_models.base import Base
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column


class TSystemFeatures(Base):
    """Table of System Features."""

    __tablename__ = 'system_features'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    system_id: Mapped[int] = mapped_column(ForeignKey("systems.id"))
    _allegiance: Mapped[str] = mapped_column(
        String, nullable=False, default=''
    )
    _security: Mapped[str] = mapped_column(
        String, nullable=False, default=''
    )
    _population: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )

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
        if (
            'SystemAllegiance' in entry
            and entry['SystemAllegiance'] != self.allegiance
        ):
            self.allegiance = entry['SystemAllegiance']
        if (
            'SystemSecurity_Localised' in entry
            and entry['SystemSecurity_Localised'] != self.security
        ):
            self.security = entry['SystemSecurity_Localised']
        if 'Population' in entry and entry['Population'] != self.population:
            self.population = entry['Population']

    @hybrid_property
    def allegiance(self) -> Optional[str]:
        """Get allegiance feature."""
        return self._allegiance

    @allegiance.setter
    def allegiance(self, value: Optional[str]):
        if self._allegiance is None or self._allegiance != value:
            self._allegiance = value

    @hybrid_property
    def population(self) -> int:
        """Get security feature."""
        return self._population

    @population.setter
    def population(self, value):
        if self._population != value:
            self._population = value

    @hybrid_property
    def security(self) -> Optional[str]:
        """Get security feature."""
        return self._security

    @security.setter
    def security(self, value: Optional[str]):
        if self._security is None or self._security != value:
            self._security = value


# #[EOF]#######################################################################

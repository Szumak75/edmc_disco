# -*- coding: UTF-8 -*-
"""
Created on 30 jan 2023.

@author: szumak@virthost.pl
"""

from typing import Optional

from disco_libs.db_models.base import DiscoBase
from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column


class TBodyFeatures(DiscoBase):
    """Table of Body Features."""

    __tablename__:str = "body_features"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    body_id: Mapped[int] = mapped_column(ForeignKey("bodies.id"))

    _absolutemagnitude: Mapped[Optional[float]] = mapped_column(
        Float(precision=6), default=None
    )
    _atmosfere: Mapped[Optional[str]] = mapped_column(String, default=None)
    _atmosferetype: Mapped[Optional[str]] = mapped_column(String, default=None)
    _axialtilt: Mapped[Optional[float]] = mapped_column(
        Float(precision=6), default=None
    )
    _body_type: Mapped[Optional[str]] = mapped_column(String, default=None)
    _discovered: Mapped[Optional[bool]] = mapped_column(Boolean, default=None)
    _discovered_first: Mapped[bool] = mapped_column(Boolean, default=False)
    _distance: Mapped[Optional[float]] = mapped_column(Float(precision=6), default=None)
    _eccentricity: Mapped[Optional[float]] = mapped_column(
        Float(precision=6), default=None
    )
    _landable: Mapped[Optional[bool]] = mapped_column(Boolean, default=None)
    _luminosity: Mapped[Optional[str]] = mapped_column(String, default=None)
    _mapped: Mapped[Optional[bool]] = mapped_column(Boolean, default=None)
    _mapped_first: Mapped[bool] = mapped_column(Boolean, default=False)
    _massem: Mapped[Optional[float]] = mapped_column(Float(precision=6), default=None)
    _orbitalinclination: Mapped[Optional[float]] = mapped_column(
        Float(precision=6), default=None
    )
    _orbitalperiod: Mapped[Optional[float]] = mapped_column(
        Float(precision=6), default=None
    )
    _periapsis: Mapped[Optional[float]] = mapped_column(
        Float(precision=6), default=None
    )
    _planet_class: Mapped[Optional[str]] = mapped_column(String, default=None)
    _radius: Mapped[Optional[float]] = mapped_column(Float(precision=6), default=None)
    _rotationperiod: Mapped[Optional[float]] = mapped_column(
        Float(precision=6), default=None
    )
    _semimajoraxis: Mapped[Optional[float]] = mapped_column(
        Float(precision=6), default=None
    )
    _star_type: Mapped[Optional[str]] = mapped_column(String, default=None)
    _stellarmass: Mapped[Optional[float]] = mapped_column(
        Float(precision=6), default=None
    )
    _subclass: Mapped[Optional[int]] = mapped_column(Integer, default=None)
    _surfacegravity: Mapped[Optional[float]] = mapped_column(
        Float(precision=6), default=None
    )
    _surfacepressure: Mapped[Optional[float]] = mapped_column(
        Float(precision=6), default=None
    )
    _surfacetemperature: Mapped[Optional[float]] = mapped_column(
        Float(precision=6), default=None
    )
    _terraformstate: Mapped[Optional[str]] = mapped_column(String, default=None)
    _volcanism: Mapped[Optional[str]] = mapped_column(String, default=None)

    def __repr__(self) -> str:
        """Return string object."""
        return (
            f"TBodyFeatures(id='{self.id}', "
            f"body_id='{self.body_id}', "
            f"absolutemagnitude='{self.absolutemagnitude or ''}', "
            f"atmosfere='{self.atmosfere or ''}', "
            f"atmosferetype='{self.atmosferetype or ''}', "
            f"axialtilt='{self.axialtilt or ''}', "
            f"body_type='{self.body_type or ''}', "
            f"discovered='{self.discovered or ''}', "
            f"discovered_first='{self.discovered_first}', "
            f"distance='{self.distance or ''}', "
            f"eccentricity='{self.eccentricity or ''}', "
            f"landable='{self.landable or ''}', "
            f"luminosity='{self.luminosity or ''}', "
            f"mapped='{self.mapped or ''}', "
            f"mapped_first='{self.mapped_first}', "
            f"massem='{self.massem or ''}', "
            f"orbitalinclination='{self.orbitalinclination or ''}', "
            f"orbitalperiod='{self.orbitalperiod or ''}', "
            f"periapsis='{self.periapsis or ''}', "
            f"planet_class='{self.planet_class or ''}', "
            f"radius='{self.radius or ''}', "
            f"rotationperiod='{self.rotationperiod or ''}', "
            f"semimajoraxis='{self.semimajoraxis or ''}', "
            f"star_type='{self.star_type or ''}', "
            f"stellarmass='{self.stellarmass or ''}', "
            f"subclass='{self.subclass or ''}', "
            f"surfacegravity='{self.surfacegravity or ''}', "
            f"surfacepressure='{self.surfacepressure or ''}', "
            f"surfacetemperature='{self.surfacetemperature or ''}', "
            f"terraformstate='{self.terraformstate or ''}', "
            f"volcanism='{self.volcanism or ''}' "
            ")"
        )

    def event_parser(self, entry: dict) -> None:
        """Event parser.

        Analyze dict from journal and import data into the object.
        """
        if (
            "AbsoluteMagnitude" in entry
            and self.absolutemagnitude != entry["AbsoluteMagnitude"]
        ):
            self.absolutemagnitude = entry["AbsoluteMagnitude"]
        if "Atmosphere" in entry and self.atmosfere != entry["Atmosphere"]:
            self.atmosfere = entry["Atmosphere"]
        if "AtmosphereType" in entry and self.atmosferetype != entry["AtmosphereType"]:
            self.atmosferetype = entry["AtmosphereType"]
        if "AxialTilt" in entry and self.axialtilt != entry["AxialTilt"]:
            self.axialtilt = entry["AxialTilt"]
        if "BodyType" in entry and self.body_type != entry["BodyType"]:
            self.body_type = entry["BodyType"]
        elif "PlanetClass" in entry:
            self.body_type = "Planet"
            self.planet_class = entry["PlanetClass"]
        elif "Cluster" in entry["BodyName"]:
            self.body_type = "Cluster"
        if "WasDiscovered" in entry and not self.discovered:
            self.discovered = entry["WasDiscovered"]
        if (
            "DistanceFromArrivalLS" in entry
            and self.distance != entry["DistanceFromArrivalLS"]
        ):
            self.distance = entry["DistanceFromArrivalLS"]
        if "Eccentricity" in entry and self.eccentricity != entry["Eccentricity"]:
            self.eccentricity = entry["Eccentricity"]
        if "Landable" in entry and self.landable != entry["Landable"]:
            self.landable = entry["Landable"]
        if "Luminosity" in entry and self.luminosity != entry["Luminosity"]:
            self.luminosity = entry["Luminosity"]
        if "WasMapped" in entry and not self.mapped:
            self.mapped = entry["WasMapped"]
        if "MassEM" in entry and self.massem != entry["MassEM"]:
            self.massem = entry["MassEM"]
        if (
            "OrbitalInclination" in entry
            and self.orbitalinclination != entry["OrbitalInclination"]
        ):
            self.orbitalinclination = entry["OrbitalInclination"]
        if "OrbitalPeriod" in entry and self.orbitalperiod != entry["OrbitalPeriod"]:
            self.orbitalperiod = entry["OrbitalPeriod"]
        if "Periapsis" in entry and self.periapsis != entry["Periapsis"]:
            self.periapsis = entry["Periapsis"]
        if "Radius" in entry and self.radius != entry["Radius"]:
            self.radius = entry["Radius"]
        if "RotationPeriod" in entry and self.rotationperiod != entry["RotationPeriod"]:
            self.rotationperiod = entry["RotationPeriod"]
        if "SemiMajorAxis" in entry and self.semimajoraxis != entry["SemiMajorAxis"]:
            self.semimajoraxis = entry["SemiMajorAxis"]
        if "StarType" in entry and self.star_type != entry["StarType"]:
            self.star_type = entry["StarType"]
        if "StellarMass" in entry and self.stellarmass != entry["StellarMass"]:
            self.stellarmass = entry["StellarMass"]
        if "Subclass" in entry and self.subclass != entry["Subclass"]:
            self.subclass = entry["Subclass"]
        if "SurfaceGravity" in entry and self.surfacegravity != entry["SurfaceGravity"]:
            self.surfacegravity = entry["SurfaceGravity"]
        if (
            "SurfacePressure" in entry
            and self.surfacepressure != entry["SurfacePressure"]
        ):
            self.surfacepressure = entry["SurfacePressure"]
        if (
            "SurfaceTemperature" in entry
            and self.surfacetemperature != entry["SurfaceTemperature"]
        ):
            self.surfacetemperature = entry["SurfaceTemperature"]
        if "TerraformState" in entry and self.terraformstate != entry["TerraformState"]:
            self.terraformstate = entry["TerraformState"]
        if "Volcanism" in entry and self.volcanism != entry["Volcanism"]:
            self.volcanism = entry["Volcanism"]

    @hybrid_property
    def absolutemagnitude(self) -> Optional[float]:
        """Get absolutemagnitude feature."""
        return self._absolutemagnitude

    @absolutemagnitude.inplace.setter
    def _absolutemagnitude_setter(self, value: Optional[float]) -> None:
        if self._absolutemagnitude != value:
            self._absolutemagnitude = value

    @hybrid_property
    def atmosfere(self) -> Optional[str]:
        """Get atmosfere feature."""
        return self._atmosfere

    @atmosfere.inplace.setter
    def _atmosfere_setter(self, value: Optional[str]) -> None:
        if self._atmosfere != value:
            self._atmosfere = value

    @hybrid_property
    def atmosferetype(self) -> Optional[str]:
        """Get atmosferetype feature."""
        return self._atmosferetype

    @atmosferetype.inplace.setter
    def _atmosferetype_setter(self, value: Optional[str]) -> None:
        if self._atmosferetype != value:
            self._atmosferetype = value

    @hybrid_property
    def axialtilt(self) -> Optional[float]:
        """Get axialtilt feature."""
        return self._axialtilt

    @axialtilt.inplace.setter
    def _axialtilt_setter(self, value: Optional[float]) -> None:
        if self._axialtilt != value:
            self._axialtilt = value

    @hybrid_property
    def body_type(self) -> Optional[str]:
        """Get bodytype feature."""
        return self._body_type

    @body_type.inplace.setter
    def _body_type_setter(self, value: Optional[str]) -> None:
        if self._body_type != value:
            self._body_type = value

    @hybrid_property
    def discovered(self) -> Optional[bool]:
        """Get discovered feature."""
        return self._discovered

    @discovered.inplace.setter
    def _discovered_setter(self, value: Optional[bool]) -> None:
        # TODO: check, first time set only
        if not self._discovered:
            self._discovered = value

    @hybrid_property
    def discovered_first(self) -> bool:
        """Get discovered_first feature."""
        return self._discovered_first

    @discovered_first.inplace.setter
    def _discovered_first_setter(self, value: bool) -> None:
        # first time set only
        if not self.discovered:
            self._discovered_first = value

    @hybrid_property
    def distance(self) -> Optional[float]:
        """Get distance feature."""
        return self._distance

    @distance.inplace.setter
    def _distance_setter(self, value: Optional[float]) -> None:
        if self._distance != value:
            self._distance = value

    @hybrid_property
    def eccentricity(self) -> Optional[float]:
        """Get eccentricity feature."""
        return self._eccentricity

    @eccentricity.inplace.setter
    def _eccentricity_setter(self, value: Optional[float]) -> None:
        if self._eccentricity != value:
            self._eccentricity = value

    @hybrid_property
    def landable(self) -> Optional[bool]:
        """Get landable feature."""
        return self._landable

    @landable.inplace.setter
    def _landable_setter(self, value: Optional[bool]) -> None:
        if self._landable != value:
            self._landable = value

    @hybrid_property
    def luminosity(self) -> Optional[str]:
        """Get luminosity feature."""
        return self._luminosity

    @luminosity.inplace.setter
    def _luminosity_setter(self, value: Optional[str]) -> None:
        if self._luminosity != value:
            self._luminosity = value

    @hybrid_property
    def mapped(self) -> Optional[bool]:
        """Get mapped feature."""
        return self._mapped

    @mapped.inplace.setter
    def _mapped_setter(self, value: Optional[bool]) -> None:
        if not self._mapped:
            self._mapped = value
            if not self.discovered and value:
                self.discovered = value

    @hybrid_property
    def mapped_first(self) -> bool:
        """Get mapped_first feature."""
        return self._mapped_first

    @mapped_first.inplace.setter
    def _mapped_first_setter(self, value: bool) -> None:
        if not self.mapped:
            self._mapped_first = value

    @hybrid_property
    def massem(self) -> Optional[float]:
        """Get massem feature."""
        return self._massem

    @massem.inplace.setter
    def _massem_setter(self, value: Optional[float]) -> None:
        if self._massem != value:
            self._massem = value

    @hybrid_property
    def orbitalinclination(self) -> Optional[float]:
        """Get orbitalinclination feature."""
        return self._orbitalinclination

    @orbitalinclination.inplace.setter
    def _orbitalinclination_setter(self, value: Optional[float]) -> None:
        if self._orbitalinclination != value:
            self._orbitalinclination = value

    @hybrid_property
    def orbitalperiod(self) -> Optional[float]:
        """Get orbitalperiod feature."""
        return self._orbitalperiod

    @orbitalperiod.inplace.setter
    def _orbitalperiod_setter(self, value: Optional[float]) -> None:
        if self._orbitalperiod != value:
            self._orbitalperiod = value

    @hybrid_property
    def periapsis(self) -> Optional[float]:
        """Get periapsis feature."""
        return self._periapsis

    @periapsis.inplace.setter
    def _periapsis_setter(self, value: Optional[float]) -> None:
        if self._periapsis is None or self._periapsis != value:
            self._periapsis = value

    @hybrid_property
    def planet_class(self) -> Optional[str]:
        """Get periapsis feature."""
        return self._planet_class

    @planet_class.inplace.setter
    def _planet_class_setter(self, value: Optional[str]) -> None:
        if self._planet_class != value:
            self._planet_class = value

    @hybrid_property
    def radius(self) -> Optional[float]:
        """Get radius feature."""
        return self._radius

    @radius.inplace.setter
    def _radius_setter(self, value: Optional[float]) -> None:
        if self._radius != value:
            self._radius = value

    @hybrid_property
    def rotationperiod(self) -> Optional[float]:
        """Get rotationperiod feature."""
        return self._rotationperiod

    @rotationperiod.inplace.setter
    def _rotationperiod_setter(self, value: Optional[float]) -> None:
        if self._rotationperiod != value:
            self._rotationperiod = value

    @hybrid_property
    def semimajoraxis(self) -> Optional[float]:
        """Get semimajoraxis feature."""
        return self._semimajoraxis

    @semimajoraxis.inplace.setter
    def _semimajoraxis_setter(self, value: Optional[float]) -> None:
        if self._semimajoraxis != value:
            self._semimajoraxis = value

    @hybrid_property
    def stellarmass(self) -> Optional[float]:
        """Get stellarmass feature."""
        return self._stellarmass

    @stellarmass.inplace.setter
    def _stellarmass_setter(self, value: Optional[float]) -> None:
        if self._stellarmass != value:
            self._stellarmass = value

    @hybrid_property
    def subclass(self) -> Optional[int]:
        """Get subclass feature."""
        return self._subclass

    @subclass.inplace.setter
    def _subclass_setter(self, value: Optional[int]) -> None:
        if self._subclass != value:
            self._subclass = value

    @hybrid_property
    def surfacegravity(self) -> Optional[float]:
        """Get surfacegravity feature."""
        return self._surfacegravity

    @surfacegravity.inplace.setter
    def _surfacegravity_setter(self, value: Optional[float]) -> None:
        if self._surfacegravity != value:
            self._surfacegravity = value

    @hybrid_property
    def surfacepressure(self) -> Optional[float]:
        """Get surfacepressure feature."""
        return self._surfacepressure

    @surfacepressure.inplace.setter
    def _surfacepressure_setter(self, value: Optional[float]) -> None:
        if self._surfacepressure != value:
            self._surfacepressure = value

    @hybrid_property
    def surfacetemperature(self) -> Optional[float]:
        """Get surfacetemperature feature."""
        return self._surfacetemperature

    @surfacetemperature.inplace.setter
    def _surfacetemperature_setter(self, value: Optional[float]) -> None:
        if self._surfacetemperature != value:
            self._surfacetemperature = value

    @hybrid_property
    def star_type(self) -> Optional[str]:
        """Get startype feature."""
        return self._star_type

    @star_type.inplace.setter
    def _star_type_setter(self, value: Optional[str]) -> None:
        if self._star_type != value:
            self._star_type = value

    @hybrid_property
    def terraformstate(self) -> Optional[str]:
        """Get terraformstate feature."""
        return self._terraformstate

    @terraformstate.inplace.setter
    def _terraformstate_setter(self, value: Optional[str]) -> None:
        if self._terraformstate != value:
            self._terraformstate = value

    @hybrid_property
    def volcanism(self) -> Optional[str]:
        """Get volcanism feature."""
        # if self._volcanism is None:
        #     return 'XXX'
        return self._volcanism

    @volcanism.inplace.setter
    def _volcanism_setter(self, value: Optional[str]) -> None:
        if self._volcanism != value:
            self._volcanism = value


# #[EOF]#######################################################################

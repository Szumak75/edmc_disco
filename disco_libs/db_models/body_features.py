# -*- coding: UTF-8 -*-
"""
Created on 30 jan 2023.

@author: szumak@virthost.pl
"""

from typing import Optional

from disco_libs.db_models.base import Base
from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column


class TBodyFeatures(Base):
    """Table of Body Features."""

    __tablename__ = 'body_features'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    body_id: Mapped[int] = mapped_column(ForeignKey("bodies.id"))

    _absolutemagnitude = mapped_column(Float(precision=6), default=None)
    _atmosfere = mapped_column(String, default=None)
    _atmosferetype = mapped_column(String, default=None)
    _axialtilt = mapped_column(Float(precision=6), default=None)
    _body_type = mapped_column(String, default=None)
    _discovered = mapped_column(Boolean, default=None)
    _discovered_first = mapped_column(Boolean, default=False)
    _distance = mapped_column(Float(precision=6), default=None)
    _eccentricity = mapped_column(Float(precision=6), default=None)
    _landable = mapped_column(Boolean, default=None)
    _luminosity = mapped_column(String, default=None)
    _mapped = mapped_column(Boolean, default=None)
    _mapped_first = mapped_column(Boolean, default=False)
    _massem = mapped_column(Float(precision=6), default=None)
    _orbitalinclination = mapped_column(Float(precision=6), default=None)
    _orbitalperiod = mapped_column(Float(precision=6), default=None)
    _periapsis = mapped_column(Float(precision=6), default=None)
    _planet_class = mapped_column(String, default=None)
    _radius = mapped_column(Float(precision=6), default=None)
    _rotationperiod = mapped_column(Float(precision=6), default=None)
    _semimajoraxis = mapped_column(Float(precision=6), default=None)
    _star_type = mapped_column(String, default=None)
    _stellarmass = mapped_column(Float(precision=6), default=None)
    _subclass = mapped_column(Integer, default=None)
    _surfacegravity = mapped_column(Float(precision=6), default=None)
    _surfacepressure = mapped_column(Float(precision=6), default=None)
    _surfacetemperature = mapped_column(Float(precision=6), default=None)
    _terraformstate = mapped_column(String, default=None)
    _volcanism = mapped_column(String, default=None)

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
            'AbsoluteMagnitude' in entry
            and self.absolutemagnitude != entry['AbsoluteMagnitude']
        ):
            self.absolutemagnitude = entry['AbsoluteMagnitude']
        if 'Atmosphere' in entry and self.atmosfere != entry['Atmosphere']:
            self.atmosfere = entry['Atmosphere']
        if (
            'AtmosphereType' in entry
            and self.atmosferetype != entry['AtmosphereType']
        ):
            self.atmosferetype = entry['AtmosphereType']
        if 'AxialTilt' in entry and self.axialtilt != entry['AxialTilt']:
            self.axialtilt = entry['AxialTilt']
        if 'BodyType' in entry and self.body_type != entry['BodyType']:
            self.body_type = entry['BodyType']
        elif 'PlanetClass' in entry:
            self.body_type = 'Planet'
            self.planet_class = entry['PlanetClass']
        elif 'Cluster' in entry['BodyName']:
            self.body_type = 'Cluster'
        if 'WasDiscovered' in entry and not self.discovered:
            self.discovered = entry['WasDiscovered']
        if (
            'DistanceFromArrivalLS' in entry
            and self.distance != entry['DistanceFromArrivalLS']
        ):
            self.distance = entry['DistanceFromArrivalLS']
        if (
            'Eccentricity' in entry
            and self.eccentricity != entry['Eccentricity']
        ):
            self.eccentricity = entry['Eccentricity']
        if 'Landable' in entry and self.landable != entry['Landable']:
            self.landable = entry['Landable']
        if 'Luminosity' in entry and self.luminosity != entry['Luminosity']:
            self.luminosity = entry['Luminosity']
        if 'WasMapped' in entry and not self.mapped:
            self.mapped = entry['WasMapped']
        if 'MassEM' in entry and self.massem != entry['MassEM']:
            self.massem = entry['MassEM']
        if (
            'OrbitalInclination' in entry
            and self.orbitalinclination != entry['OrbitalInclination']
        ):
            self.orbitalinclination = entry['OrbitalInclination']
        if (
            'OrbitalPeriod' in entry
            and self.orbitalperiod != entry['OrbitalPeriod']
        ):
            self.orbitalperiod = entry['OrbitalPeriod']
        if 'Periapsis' in entry and self.periapsis != entry['Periapsis']:
            self.periapsis = entry['Periapsis']
        if 'Radius' in entry and self.radius != entry['Radius']:
            self.radius = entry['Radius']
        if (
            'RotationPeriod' in entry
            and self.rotationperiod != entry['RotationPeriod']
        ):
            self.rotationperiod = entry['RotationPeriod']
        if (
            'SemiMajorAxis' in entry
            and self.semimajoraxis != entry['SemiMajorAxis']
        ):
            self.semimajoraxis = entry['SemiMajorAxis']
        if 'StarType' in entry and self.star_type != entry['StarType']:
            self.star_type = entry['StarType']
        if (
            'StellarMass' in entry
            and self.stellarmass != entry['StellarMass']
        ):
            self.stellarmass = entry['StellarMass']
        if 'Subclass' in entry and self.subclass != entry['Subclass']:
            self.subclass = entry['Subclass']
        if (
            'SurfaceGravity' in entry
            and self.surfacegravity != entry['SurfaceGravity']
        ):
            self.surfacegravity = entry['SurfaceGravity']
        if (
            'SurfacePressure' in entry
            and self.surfacepressure != entry['SurfacePressure']
        ):
            self.surfacepressure = entry['SurfacePressure']
        if (
            'SurfaceTemperature' in entry
            and self.surfacetemperature != entry['SurfaceTemperature']
        ):
            self.surfacetemperature = entry['SurfaceTemperature']
        if (
            'TerraformState' in entry
            and self.terraformstate != entry['TerraformState']
        ):
            self.terraformstate = entry['TerraformState']
        if 'Volcanism' in entry and self.volcanism != entry['Volcanism']:
            self.volcanism = entry['Volcanism']

    @hybrid_property
    def absolutemagnitude(self) -> Optional[Float]:
        """Get absolutemagnitude feature."""
        return self._absolutemagnitude

    @absolutemagnitude.setter
    def absolutemagnitude(self, value):
        if (
            self._absolutemagnitude is None
            or self._absolutemagnitude != value
        ):
            self._absolutemagnitude = value

    @hybrid_property
    def atmosfere(self) -> Optional[str]:
        """Get atmosfere feature."""
        return self._atmosfere

    @atmosfere.setter
    def atmosfere(self, value):
        if self._atmosfere is None or self._atmosfere != value:
            self._atmosfere = value

    @hybrid_property
    def atmosferetype(self) -> Optional[str]:
        """Get atmosferetype feature."""
        return self._atmosferetype

    @atmosferetype.setter
    def atmosferetype(self, value):
        if self._atmosferetype is None or self._atmosferetype != value:
            self._atmosferetype = value

    @hybrid_property
    def axialtilt(self) -> Optional[Float]:
        """Get axialtilt feature."""
        return self._axialtilt

    @axialtilt.setter
    def axialtilt(self, value):
        if self._axialtilt is None or self._axialtilt != value:
            self._axialtilt = value

    @hybrid_property
    def body_type(self) -> Optional[str]:
        """Get bodytype feature."""
        return self._body_type

    @body_type.setter
    def body_type(self, value):
        if self._body_type is None or self._body_type != value:
            self._body_type = value

    @hybrid_property
    def discovered(self) -> Optional[bool]:
        """Get discovered feature."""
        return self._discovered

    @discovered.setter
    def discovered(self, value):
        if not self._discovered:
            self._discovered = value

    @hybrid_property
    def discovered_first(self) -> bool:
        """Get discovered_first feature."""
        return self._discovered_first

    @discovered_first.setter
    def discovered_first(self, value):
        if not self.discovered:
            self._discovered_first = value

    @hybrid_property
    def distance(self) -> Optional[Float]:
        """Get distance feature."""
        return self._distance

    @distance.setter
    def distance(self, value):
        if self._distance is None or self._distance != value:
            self._distance = value

    @hybrid_property
    def eccentricity(self) -> Optional[Float]:
        """Get eccentricity feature."""
        return self._eccentricity

    @eccentricity.setter
    def eccentricity(self, value):
        if self._eccentricity is None or self._eccentricity != value:
            self._eccentricity = value

    @hybrid_property
    def landable(self) -> Optional[bool]:
        """Get landable feature."""
        return self._landable

    @landable.setter
    def landable(self, value):
        if self._landable is None or self._landable != value:
            self._landable = value

    @hybrid_property
    def luminosity(self) -> Optional[str]:
        """Get luminosity feature."""
        return self._luminosity

    @luminosity.setter
    def luminosity(self, value):
        if self._luminosity is None or self._luminosity != value:
            self._luminosity = value

    @hybrid_property
    def mapped(self) -> Optional[bool]:
        """Get mapped feature."""
        return self._mapped

    @mapped.setter
    def mapped(self, value):
        if not self._mapped:
            self._mapped = value
            if not self.discovered and value:
                self.discovered = value

    @hybrid_property
    def mapped_first(self) -> bool:
        """Get mapped_first feature."""
        return self._mapped_first

    @mapped_first.setter
    def mapped_first(self, value):
        if not self.mapped:
            self._mapped_first = value

    @hybrid_property
    def massem(self) -> Optional[Float]:
        """Get massem feature."""
        return self._massem

    @massem.setter
    def massem(self, value):
        if self._massem is None or self._massem != value:
            self._massem = value

    @hybrid_property
    def orbitalinclination(self) -> Optional[Float]:
        """Get orbitalinclination feature."""
        return self._orbitalinclination

    @orbitalinclination.setter
    def orbitalinclination(self, value):
        if (
            self._orbitalinclination is None
            or self._orbitalinclination != value
        ):
            self._orbitalinclination = value

    @hybrid_property
    def orbitalperiod(self) -> Optional[Float]:
        """Get orbitalperiod feature."""
        return self._orbitalperiod

    @orbitalperiod.setter
    def orbitalperiod(self, value):
        if self._orbitalperiod is None or self._orbitalperiod != value:
            self._orbitalperiod = value

    @hybrid_property
    def periapsis(self) -> Optional[Float]:
        """Get periapsis feature."""
        return self._periapsis

    @periapsis.setter
    def periapsis(self, value):
        if self._periapsis is None or self._periapsis != value:
            self._periapsis = value

    @hybrid_property
    def planet_class(self) -> Optional[str]:
        """Get periapsis feature."""
        return self._planet_class

    @planet_class.setter
    def planet_class(self, value):
        if self._planet_class is None or self._planet_class != value:
            self._planet_class = value

    @hybrid_property
    def radius(self) -> Optional[Float]:
        """Get radius feature."""
        return self._radius

    @radius.setter
    def radius(self, value):
        if self._radius is None or self._radius != value:
            self._radius = value

    @hybrid_property
    def rotationperiod(self) -> Optional[Float]:
        """Get rotationperiod feature."""
        return self._rotationperiod

    @rotationperiod.setter
    def rotationperiod(self, value):
        if self._rotationperiod is None or self._rotationperiod != value:
            self._rotationperiod = value

    @hybrid_property
    def semimajoraxis(self) -> Optional[Float]:
        """Get semimajoraxis feature."""
        return self._semimajoraxis

    @semimajoraxis.setter
    def semimajoraxis(self, value):
        if self._semimajoraxis is None or self._semimajoraxis != value:
            self._semimajoraxis = value

    @hybrid_property
    def stellarmass(self) -> Optional[Float]:
        """Get stellarmass feature."""
        return self._stellarmass

    @stellarmass.setter
    def stellarmass(self, value):
        if self._stellarmass is None or self._stellarmass != value:
            self._stellarmass = value

    @hybrid_property
    def subclass(self) -> Optional[int]:
        """Get subclass feature."""
        return self._subclass

    @subclass.setter
    def subclass(self, value):
        if self._subclass is None or self._subclass != value:
            self._subclass = value

    @hybrid_property
    def surfacegravity(self) -> Optional[Float]:
        """Get surfacegravity feature."""
        return self._surfacegravity

    @surfacegravity.setter
    def surfacegravity(self, value):
        if self._surfacegravity is None or self._surfacegravity != value:
            self._surfacegravity = value

    @hybrid_property
    def surfacepressure(self) -> Optional[Float]:
        """Get surfacepressure feature."""
        return self._surfacepressure

    @surfacepressure.setter
    def surfacepressure(self, value):
        if self._surfacepressure is None or self._surfacepressure != value:
            self._surfacepressure = value

    @hybrid_property
    def surfacetemperature(self) -> Optional[Float]:
        """Get surfacetemperature feature."""
        return self._surfacetemperature

    @surfacetemperature.setter
    def surfacetemperature(self, value):
        if (
            self._surfacetemperature is None
            or self._surfacetemperature != value
        ):
            self._surfacetemperature = value

    @hybrid_property
    def star_type(self) -> Optional[str]:
        """Get startype feature."""
        return self._star_type

    @star_type.setter
    def star_type(self, value):
        if self._star_type is None or self._star_type != value:
            self._star_type = value

    @hybrid_property
    def terraformstate(self) -> Optional[str]:
        """Get terraformstate feature."""
        return self._terraformstate

    @terraformstate.setter
    def terraformstate(self, value):
        if self._terraformstate is None or self._terraformstate != value:
            self._terraformstate = value

    @hybrid_property
    def volcanism(self) -> Optional[str]:
        """Get volcanism feature."""
        # if self._volcanism is None:
        #     return 'XXX'
        return self._volcanism

    @volcanism.setter
    def volcanism(self, value):
        if self._volcanism is None or self._volcanism != value:
            self._volcanism = value


# #[EOF]#######################################################################

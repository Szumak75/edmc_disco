# -*- coding: UTF-8 -*-
"""
Created on 30 jan 2023.

@author: szumak@virthost.pl
"""

import datetime
import time
from typing import List, Optional, Union, Dict, List

from disco_libs.db_models.base import DiscoBase
from disco_libs.db_models.body import TBody
from disco_libs.db_models.body_features import TBodyFeatures
from disco_libs.db_models.system_features import TSystemFeatures
from sqlalchemy import Float, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship


class TSystem(DiscoBase):
    """Table of Systems."""

    __tablename__ = "systems"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False, default="")
    systemaddress: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    pos_x: Mapped[float] = mapped_column(Float(precision=5), nullable=False)
    pos_y: Mapped[float] = mapped_column(Float(precision=5), nullable=False)
    pos_z: Mapped[float] = mapped_column(Float(precision=5), nullable=False)
    bodycount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    nonbodycount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    features: Mapped["TSystemFeatures"] = relationship("TSystemFeatures")
    bodies: Mapped[List["TBody"]] = relationship("TBody")
    _timestamp: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    def __init__(self):
        """Initialize object."""
        DiscoBase.__init__(self)
        self.features = TSystemFeatures()

    def __repr__(self) -> str:
        """Return string object."""
        return (
            f"TSystem(id='{self.id}', "
            f"name='{self.name}', "
            f"systemaddress='{self.systemaddress}', "
            f"coords=[{self.pos_x}, {self.pos_y}, {self.pos_z}], "
            f"bodycount='{self.bodycount}', "
            f"nonbodycount='{self.nonbodycount}', "
            f"features='{self.features or ''}', "
            f"bodies='{self.bodies or ''}', "
            f"timestamp='{self.timestamp}' "
            ")"
        )

    def event_parser(self, entry: Dict) -> bool:
        """Event parser.

        Analyze dict from journal and import data into the object.
        """
        ret = False
        if "SystemAddress" in entry:
            ret = True
            self.systemaddress = entry["SystemAddress"]
        if "StarSystem" in entry:
            ret = True
            self.name = entry["StarSystem"]
        if "timestamp" in entry:
            ret = True
            self.timestamp = entry["timestamp"]
        if "StarPos" in entry:
            ret = True
            self.star_pos = entry["StarPos"]
        return ret

    def get_body(self, body_id: int) -> Optional[TBody]:
        """Return a TBody object with the specified BodyID or None."""
        if not self.bodies:
            return None
        body = None
        for item in self.bodies:
            if item.bodyid == body_id:
                body = item
                break
        return body

    @hybrid_property
    def star_pos(self) -> List:
        """Get 'StarPos' list."""
        return [self.pos_x, self.pos_y, self.pos_z]

    @star_pos.setter
    def star_pos(self, data: List):
        """Set 'StarPos' from list."""
        if isinstance(data, List) and len(data) == 3:
            self.pos_x = data[0]
            self.pos_y = data[1]
            self.pos_z = data[2]
        else:
            print(f"Something is wrong with StarPos: {data} for {self.name}")

    @hybrid_property
    def timestamp(self) -> int:
        """Get latest data timestamp."""
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: Union[int, str]):
        if isinstance(value, int):
            self._timestamp = value
        else:
            # create struct_time
            str_time = time.strptime(value, "%Y-%m-%dT%H:%M:%SZ")

            # create datetime object
            dt_obj = datetime.datetime(*str_time[:6])

            self._timestamp = int(dt_obj.timestamp())

    @property
    def scanned_body_count(self) -> int:
        """Return number of discovered body."""
        count: int = 0
        for item in self.bodies:
            body: TBody = item
            features: TBodyFeatures = body.features
            if features.star_type:
                count += 1
                continue
            if features.body_type and features.body_type == "Planet":
                count += 1
                continue

        return count

    @property
    def progress(self) -> str:
        """Return discovery progress formated string."""
        return f"{self.scanned_body_count}/{self.bodycount}"


# #[EOF]#######################################################################

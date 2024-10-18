# -*- coding: UTF-8 -*-
"""
Created on 30 jan 2023.

@author: szumak@virthost.pl
"""

from typing import List, Dict, Optional

from sqlalchemy import ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from disco.jsktoolbox.edmctool.ed_keys import EDKeys
from disco.db_models.base import DiscoBase


class TGenusScan(DiscoBase):
    """Table of Genus Scan."""

    __tablename__: str = "genus_scan"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    genuses_id: Mapped[int] = mapped_column(ForeignKey("genuses.id"))
    species: Mapped[str] = mapped_column(String)
    species_localised: Mapped[str] = mapped_column(String)
    variant: Mapped[str] = mapped_column(String, default="")
    variant_localised: Mapped[str] = mapped_column(String, default="")
    count: Mapped[int] = mapped_column(Integer, default=0)
    done: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        """Return string object."""
        return (
            f"TGenusScan(id='{self.id}', "
            f"genuses_id='{self.genuses_id}', "
            f"species='{self.species}', "
            f"species_localised='{self.species_localised}', "
            f"variant='{self.variant}', "
            f"variant_localised='{self.variant_localised}', "
            f"count='{self.count}', "
            f"done='{self.done}' "
            ")"
        )


class TGenus(DiscoBase):
    """Table of Genuses."""

    __tablename__: str = "genuses"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    body_genuses_id: Mapped[int] = mapped_column(ForeignKey("body_genuses.id"))
    genus: Mapped[str] = mapped_column(String)
    genus_localised: Mapped[str] = mapped_column(String)
    scan: Mapped[List["TGenusScan"]] = relationship("TGenusScan")

    def __repr__(self) -> str:
        """Return string object."""
        return (
            f"TGenus(id='{self.id}', "
            f"body_genuses_id='{self.body_genuses_id}', "
            f"genus='{self.genus}', "
            f"genus_localised='{self.genus_localised}', "
            f"scan='{self.scan or ''}' "
            ")"
        )


class TBodyGenuses(DiscoBase):
    """Table of Body Genuses."""

    __tablename__: str = "body_genuses"

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    body_id: Mapped[int] = mapped_column(ForeignKey("bodies.id"))
    genuses: Mapped[List["TGenus"]] = relationship("TGenus")

    def __repr__(self) -> str:
        """Return string object."""
        return (
            f"TBodyGenuses(id='{self.id}', "
            f"body_id='{self.body_id}', "
            f"genuses='{self.genuses}' "
            ")"
        )

    def event_parser(self, entry: Dict) -> bool:
        """Event parser.

        Analyse dict from journal and import data into the object.
        """
        ret = False
        if EDKeys.GENUSES in entry and entry[EDKeys.GENUSES]:
            for e_genus in entry[EDKeys.GENUSES]:
                test = False
                for item in self.genuses:
                    if (
                        item.genus == e_genus[EDKeys.GENUS]
                        and item.genus_localised == e_genus[EDKeys.GENUS_LOCALISED]
                    ):
                        test = True
                        ret = True
                if not test:
                    tmp = TGenus()
                    tmp.genus = e_genus[EDKeys.GENUS]
                    tmp.genus_localised = e_genus[EDKeys.GENUS_LOCALISED]
                    self.genuses.append(tmp)
                    ret = True
        elif entry[EDKeys.EVENT] == EDKeys.SCAN_ORGANIC:
            for item in self.genuses:
                genuses: TGenus = item

                if (
                    genuses.genus == entry[EDKeys.GENUS]
                    and genuses.genus_localised == entry[EDKeys.GENUS_LOCALISED]
                ):
                    scan: Optional[TGenusScan] = None
                    if entry.get(EDKeys.VARIANT, "") != "":
                        # search for scan with variant
                        for item_scan in genuses.scan:
                            if (
                                item_scan.variant_localised
                                == entry[EDKeys.VARIANT_LOCALISED]
                            ):
                                scan = item_scan
                                break

                    else:
                        # search for scan without variant
                        for item_scan in genuses.scan:
                            if (
                                item_scan.species_localised
                                == entry[EDKeys.SPECIES_LOCALISED]
                            ):
                                scan = item_scan
                                break
                    if not scan:
                        scan = TGenusScan()
                        scan.species = entry[EDKeys.SPECIES]
                        scan.species_localised = entry[EDKeys.SPECIES_LOCALISED]
                        scan.variant = entry.get(EDKeys.VARIANT, "")
                        scan.variant_localised = entry.get(EDKeys.VARIANT_LOCALISED, "")
                        genuses.scan.append(scan)

                    if scan.done:
                        ret = True
                        break
                    if entry[EDKeys.SCAN_TYPE] == EDKeys.LOG:
                        scan.count = 1
                    elif entry[EDKeys.SCAN_TYPE] == EDKeys.SAMPLE:
                        scan.count += 1
                    if entry[EDKeys.SCAN_TYPE] == EDKeys.ANALYSE:
                        scan.done = True

                    ret = True
                    break

        return ret


# #[EOF]#######################################################################

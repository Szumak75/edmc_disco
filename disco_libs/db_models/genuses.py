# -*- coding: UTF-8 -*-
"""
Created on 30 jan 2023.

@author: szumak@virthost.pl
"""

from typing import List, Dict

from sqlalchemy import ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from disco_libs.db_models.base import Base


class TGenusScan(Base):
    """Table of Genus Scan."""

    __tablename__ = 'genus_scan'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    genuses_id: Mapped[int] = mapped_column(ForeignKey("genuses.id"))
    species: Mapped[str] = mapped_column(String)
    species_localised: Mapped[str] = mapped_column(String)
    variant: Mapped[str] = mapped_column(String, default='')
    variant_localised: Mapped[str] = mapped_column(String, default='')
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


class TGenus(Base):
    """Table of Genuses."""

    __tablename__ = 'genuses'

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    body_genuses_id: Mapped[int] = mapped_column(
        ForeignKey("body_genuses.id")
    )
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


class TBodyGenuses(Base):
    """Table of Body Genuses."""

    __tablename__ = 'body_genuses'

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
        if 'Genuses' in entry and entry['Genuses']:
            for egenuse in entry['Genuses']:
                test = False
                for item in self.genuses:
                    if (
                        item.genus == egenuse['Genus']
                        and item.genus_localised
                        == egenuse['Genus_Localised']
                    ):
                        test = True
                        ret = True
                if not test:
                    tmp = TGenus()
                    tmp.genus = egenuse['Genus']
                    tmp.genus_localised = egenuse['Genus_Localised']
                    self.genuses.append(tmp)
                    ret = True
        elif entry['event'] == 'ScanOrganic':
            for item in self.genuses:
                genuses: TGenus = item

                if (
                    genuses.genus == entry['Genus']
                    and genuses.genus_localised == entry['Genus_Localised']
                ):
                    scan = None
                    if entry.get('Variant', '') != '':
                        # search for scan with variant
                        for item_scan in genuses.scan:
                            iscan: TGenusScan = item_scan
                            if (
                                iscan.variant_localised
                                == entry['Variant_Localised']
                            ):
                                scan = iscan
                                break

                    else:
                        # search for scan without variant
                        for item_scan in genuses.scan:
                            iscan: TGenusScan = item_scan
                            if (
                                iscan.species_localised
                                == entry['Species_Localised']
                            ):
                                scan = iscan
                                break
                    if not scan:
                        scan = TGenusScan()
                        scan.species = entry['Species']
                        scan.species_localised = entry['Species_Localised']
                        scan.variant = entry.get('Variant', '')
                        scan.variant_localised = entry.get(
                            'Variant_Localised', ''
                        )
                        genuses.scan.append(scan)

                    if scan.done:
                        ret = True
                        break
                    if entry['ScanType'] == 'Log':
                        scan.count = 1
                    elif entry['ScanType'] == 'Sample':
                        scan.count += 1
                    if entry['ScanType'] == 'Analyse':
                        scan.done = True

                    ret = True
                    break

        return ret


# #[EOF]#######################################################################

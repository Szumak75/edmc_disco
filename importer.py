#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 18.12.2023

  Purpose: database importer for data from journal files.
"""


import json
from sys import stdin

from disco.jsktoolbox.edmctool.ed_keys import EDKeys
from disco.database import Database, DBProcessor

if __name__ == "__main__":
    print("Starting Journal Importer")

    processor = DBProcessor(Database(False).session)
    counter = 0

    for line in stdin:
        counter += 1
        entry = json.loads(line)
        if EDKeys.EVENT in entry:
            out = None
            # print(entry)
            # if entry['event'] in ('FSDJump', 'Scan', ):
            #     print(f"{counter}: {entry}")
            #     print('')
            if entry[EDKeys.EVENT] == EDKeys.FSD_JUMP:
                out = processor.add_system(entry)
                # print(f"{counter}::::{out}")
            elif entry[EDKeys.EVENT] == EDKeys.SCAN and entry["ScanType"] in (
                "AutoScan",
                "Detailed",
                "Basic",
                "NavBeaconDetail",
            ):
                out = processor.add_body(entry)
            elif entry[EDKeys.EVENT] == "FSSDiscoveryScan":
                out = processor.update_system(entry)
            elif entry[EDKeys.EVENT] == "FSSBodySignals":
                out = processor.add_signal(entry)
            elif entry[EDKeys.EVENT] == "SAASignalsFound":
                processor.add_signal(entry)
                out = processor.add_genus(entry)
            elif entry[EDKeys.EVENT] == "CodexEntry":
                # print(f"XXXX:::{entry}:::XXXX")
                out = processor.add_codex(entry)
                # print(f"{counter}::::{out}")
            elif entry[EDKeys.EVENT] == "ScanOrganic":
                # print(f"XXXX:::{entry}:::XXXX")
                out = processor.add_genus(entry)
                # print(f"{counter}::::{out}")
            elif entry[EDKeys.EVENT] == "SAAScanComplete":
                out = processor.mapped_body(entry)

            if out:
                print(f"[{counter}]: id:{out.systemaddress}, name:{out.name}")

        processor.close()


# #[EOF]#######################################################################

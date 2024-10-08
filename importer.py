#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 18.12.2023

  Purpose: database importer for data from journal files.
"""


import json
from sys import stdin

from disco.database import Database, DBProcessor

if __name__ == "__main__":
    print("Starting Journal Importer")

    processor = DBProcessor(Database(False).session)
    counter = 0

    for line in stdin:
        counter += 1
        entry = json.loads(line)
        if "event" in entry:
            out = None
            # print(entry)
            # if entry['event'] in ('FSDJump', 'Scan', ):
            #     print(f"{counter}: {entry}")
            #     print('')
            if entry["event"] == "FSDJump":
                out = processor.add_system(entry)
                # print(f"{counter}::::{out}")
            elif entry["event"] == "Scan" and entry["ScanType"] in (
                "AutoScan",
                "Detailed",
                "Basic",
                "NavBeaconDetail",
            ):
                out = processor.add_body(entry)
            elif entry["event"] == "FSSDiscoveryScan":
                out = processor.update_system(entry)
            elif entry["event"] == "FSSBodySignals":
                out = processor.add_signal(entry)
            elif entry["event"] == "SAASignalsFound":
                processor.add_signal(entry)
                out = processor.add_genus(entry)
            elif entry["event"] == "CodexEntry":
                # print(f"XXXX:::{entry}:::XXXX")
                out = processor.add_codex(entry)
                # print(f"{counter}::::{out}")
            elif entry["event"] == "ScanOrganic":
                # print(f"XXXX:::{entry}:::XXXX")
                out = processor.add_genus(entry)
                # print(f"{counter}::::{out}")
            elif entry["event"] == "SAAScanComplete":
                out = processor.mapped_body(entry)

            if out:
                print(f"[{counter}]: id:{out.systemaddress}, name:{out.name}")

        processor.close()


# #[EOF]#######################################################################

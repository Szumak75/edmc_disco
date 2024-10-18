#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 18.12.2023

  Purpose: database importer for data from journal files.
"""


import json
from sys import stdin
from typing import Dict

from disco.jsktoolbox.edmctool.ed_keys import EDKeys


def formatter(item: str) -> str:
    return item.upper()


if __name__ == "__main__":
    # print("Starting Journal keys extractor.")

    counter = 0
    keys: Dict = {}

    for line in stdin:
        counter += 1
        entry = json.loads(line)
        if isinstance(entry, Dict):
            for item in entry.keys():
                if item not in keys:
                    keys[item] = 0

    # print(sorted(keys.keys()))
    for key in sorted(keys.keys()):
        tmp = ""
        for char in key:
            if char.isupper() and tmp:
                tmp += "_"
            tmp += char
        tmp = tmp.replace("__", "_")
        print(f"{formatter(tmp)}:str='{key}'")


# #[EOF]#######################################################################

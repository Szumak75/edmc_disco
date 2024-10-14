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

if __name__ == "__main__":
    print("Starting Journal keys extractor.")

    counter = 0

    for line in stdin:
        counter += 1
        entry = json.loads(line)


# #[EOF]#######################################################################

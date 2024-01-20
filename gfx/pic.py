# -*- coding: UTF-8 -*-

import base64


def conv(filename: str) -> None:
    fh = open(filename, "rb")
    print(f"        {filename}: bytes = {base64.b64encode(fh.read())}")
    print("")


files: list[str] = [
    "belt-16.png",
    "blackhole-16.png",
    "gassy-16.png",
    "genomic-16.png",
    "geologic-16.png",
    "neutron-16.png",
    "planet-16.png",
    "planet-atm-16.png",
    "planet-earthlike-16.png",
    "rocky-16.png",
    "rocky-atm-16.png",
    "scan-planet-16.png",
    "scan-planet-atm-16.png",
    "scan-genomic-16.png",
    "scan-geologic-16.png",
    "scan-genomic-geologic-16.png",
    "star-16.png",
    "landable-16.png",
    "distance-16.png",
    "humans-16.png",
    "scoopable-16.png",
    "temp-16.png",
    "map-16.png",
    "first-16.png",
    "dollar-16.png",
    "terraforming-16.png",
]

for item in files:
    conv(item)

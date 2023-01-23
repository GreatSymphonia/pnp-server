#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Model:
    def __init__(self, image: str):
        self.image: str = image


PLATFORMS = {
    'C9300-24P': Model(
        image='CAT9K',
    ),
    'C9500-24Q': Model(
        image='CAT9K',
    ),
    'ASR1001-HX': Model(
        image='ASR1000',
    ),
    'C1117-4PMLTEEAWE': Model(
        # image='C1100_16_12',
        # image='C1100_17_09',
        image='C1100_17_06_04',
    ),
    'C1000-8T-2G-L': Model(
        image='C1000_15_02',
    ),
    'C1000-24P-4G-L': Model(
        image='C1000_15_02',
    ),
    'C1000-24T-4G-L': Model(
        image='C1000_15_02',
    ),
    'C1000-24T-4X-L': Model(
        image='C1000_15_02',
    ),
    'C1000-48P-4G-L': Model(
        image='C1000_15_02',
    ),
    'C1000-48T-4X-L': Model(
        image='C1000_15_02',
    ),
    'WS-C3560CX-12PD-S': Model(
        image='C3560CX',
    ),
}

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
        image='C1100_16_12',
        # image='C1100_17_01',
        # image='C1100_17_09',
        # image='C1100_17_06_04',

    ),
}

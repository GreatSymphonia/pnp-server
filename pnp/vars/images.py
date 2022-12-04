#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class SoftwareImage:
    def __init__(self, version: str, image: str, md5: str, size: int):
        self.image: str = image
        self.version: str = version
        self.md5: str = md5
        self.size: int = size


IMAGES = {
    'CAT9K': SoftwareImage(
        image='cat9k_iosxe.17.06.01.SPA.bin',
        version='17.6.1',
        md5='fdb9c92bae37f9130d0ee6761afe2919',
        size=1,
    ),
    'ASR1000': SoftwareImage(
        image='asr1000-universalk9.17.05.01a.SPA.bin',
        version='17.5.1a',
        md5='0e4b1fc1448f8ee289634a41f75dc215',
        size=1,
    ),
    'C1100_16_12': SoftwareImage(
        image='c1100-universalk9.16.12.01a.SPA.bin',
        version='16.12.1a',
        md5='045d73625025b4f77c65c7800b7faa2b',
        size=541469788,
    ),
    'C1100_17_01': SoftwareImage(
        image='c1100-universalk9.17.01.01.SPA.bin',
        version='17.1.1',
        md5='62e79c54994b82fc862c2ca043dcd543',
        size=573996288,
    ),
    'C1100_17_02': SoftwareImage(
        image='c1100-universalk9.17.02.03.SPA.bin',
        version='17.2.3',
        md5='4986d253b333d21b1b80c76f6d2267ca',
        size=589675224,
        # size=5896752240000,
    ),
    'C1100_17_03': SoftwareImage(
        image='c1100-universalk9.17.03.05.SPA.bin',
        version='17.3.5',
        md5='64aa0df0806f7f962d66d325ff917e4a',
        size=604409868,
    ),
    'C1100_17_04': SoftwareImage(
        image='c1100-universalk9.17.04.02.SPA.bin',
        version='17.4.2',
        md5='40b7ec81c4e4cdc8b3683a3938ae8361',
        size=651402492,
    ),
    'C1100_17_05': SoftwareImage(
        image='c1100-universalk9.17.05.01a.SPA.bin',
        version='17.5.1a',
        md5='85d86916e33d27ae9867eec822206b97',
        size=674793716,
    ),
    'C1100_17_06_03': SoftwareImage(
        image='c1100-universalk9.17.06.03a.SPA.bin',
        version='17.6.3a',
        md5='2501b21b6fa3f71ea6acd7d59bcc8423',
        size=706422748,
    ),
    'C1100_17_06_04': SoftwareImage(
        image='c1100-universalk9.17.06.04.SPA.bin',
        version='17.6.4',
        md5='2caa962f5ed0ecc52f99b90c733c54de',
        size=706565772,
    ),
    'C1100_17_07': SoftwareImage(
        image='c1100-universalk9.17.07.02.SPA.bin',
        version='17.7.2',
        md5='b824743e09cfa2644ccb442ef3e48cd2',
        size=727305300,
    ),
    'C1100_17_08': SoftwareImage(
        image='c1100-universalk9.17.08.01a.SPA.bin',
        version='17.8.1a',
        md5='8997c56cb03b5dcb08f12bf82fe23988',
        size=758605624,
    ),
    'C1100_17_09': SoftwareImage(
        image='c1100-universalk9.17.09.01a.SPA.bin',
        version='17.9.1a',
        md5='b3efb230d869fa6e77a98b4130c89585',
        size=684976080,
    ),
}

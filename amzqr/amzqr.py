#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Positional parameters
#   words: str
#
# Optional parameters
#   version: int, from 1 to 40
#   level: str, just one of ('L','M','Q','H')
#   picutre: str, a filename of a image
#   colorized: bool
#   constrast: float
#   brightness: float
#   save_name: str, the output filename like 'example.png'
#   save_dir: str, the output directory
#
# See [https://github.com/hwxhw/amazing-qr] for more details!

import os
from amzqr.utils.QRCodeConfig import QRCodeConfig
from amzqr.utils.qrcode_maker.QRCodeMakerFactory import QRCodeMakerFactory

def run(words, version=1, level='H', picture=None, colorized=False, contrast=1.0, brightness=1.0, save_name=None, save_dir=os.getcwd()):
    myConfig = QRCodeConfig(words, version, level, picture, colorized, contrast, brightness, save_name, save_dir)
    maker = QRCodeMakerFactory(myConfig)
    ver, ecl, qr_name = maker.run()
    return ver, ecl, qr_name
# -*- coding: utf-8 -*-

from PIL import Image
import os

class QRCodeDrawer:
    UNIT_LEN = 3
    BACKGROUND_COLOR = 'white'
    PIC_NAME = 'qrcode.png'

    @staticmethod
    def draw_qrcode(abspath, qrmatrix):
        x = y = 4*QRCodeDrawer.UNIT_LEN
        pic = Image.new('1', [(len(qrmatrix)+8)*QRCodeDrawer.UNIT_LEN]*2, QRCodeDrawer.BACKGROUND_COLOR)
        
        for line in qrmatrix:
            for module in line:
                if module:
                    QRCodeDrawer._draw_a_black_unit(pic, x, y, QRCodeDrawer.UNIT_LEN)
                x += QRCodeDrawer.UNIT_LEN
            x, y = 4*QRCodeDrawer.UNIT_LEN, y+QRCodeDrawer.UNIT_LEN

        saving = os.path.join(abspath, QRCodeDrawer.PIC_NAME)
        pic.save(saving)
        return saving
    
    @staticmethod
    def _draw_a_black_unit(p, x, y, ul):
        for i in range(ul):
            for j in range(ul):
                p.putpixel((x+i, y+j), 0)
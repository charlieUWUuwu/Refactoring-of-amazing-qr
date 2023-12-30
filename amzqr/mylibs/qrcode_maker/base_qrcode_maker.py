from amzqr.mylibs.qrcode_config import QRCodeConfig
from PIL import Image
from typing import Tuple

import abc
import os

class BaseQRCodeMaker(abc.ABC):
    def __init__(self, params: QRCodeConfig):
        self._params = params

    @abc.abstractmethod
    def run(self) -> Tuple[int, str, str]:
        raise NotImplementedError
    
    def _make_tempdir(self):
        tempdir = os.path.join(os.path.expanduser('~'), '.myqr') 
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)   
        return tempdir
    
    def _get_qrcode(self, dir):
        from amzqr.mylibs.theqrmodule import TheQRModule
        new_ver, qr_name = TheQRModule.get_qrcode(self._params.version, self._params.level, self._params.words, dir)
        return new_ver, qr_name
    
    def _combine(self, ver, qr_name, bg_name, save_dir, save_name=None):
        from amzqr.mylibs.constant import alig_location
        from PIL import ImageEnhance

        qr = Image.open(qr_name)
        qr = qr.convert('RGBA') if self._params.colorized else qr
        bg0 = Image.open(bg_name).convert('RGBA')
        bg0 = ImageEnhance.Contrast(bg0).enhance(self._params.contrast)
        bg0 = ImageEnhance.Brightness(bg0).enhance(self._params.brightness)

        # 調整背景圖片的大小以適應 QR 碼圖片的大小
        if bg0.size[0] < bg0.size[1]:
            bg0 = bg0.resize((qr.size[0]-24, (qr.size[0]-24)*int(bg0.size[1]/bg0.size[0])))
        else:
            bg0 = bg0.resize(((qr.size[1]-24)*int(bg0.size[0]/bg0.size[1]), qr.size[1]-24))    
        bg = bg0 if self._params.colorized else bg0.convert('1')
        
        # 初始化用於定位 QR 碼對齊圖案的列表
        aligs = []
        if ver > 1:
            aloc = alig_location[ver-2]
            for a in range(len(aloc)):
                for b in range(len(aloc)):
                    if not ((a==b==0) or (a==len(aloc)-1 and b==0) or (a==0 and b==len(aloc)-1)):
                        for i in range(3*(aloc[a]-2), 3*(aloc[a]+3)):
                            for j in range(3*(aloc[b]-2), 3*(aloc[b]+3)):
                                aligs.append((i,j))

        # 將背景圖片與 QR 碼圖片結合，並回傳圖片名
        for i in range(qr.size[0]-24):
            for j in range(qr.size[1]-24):
                if not ((i in (18,19,20)) or (j in (18,19,20)) or (i<24 and j<24) or (i<24 and j>qr.size[1]-49) or (i>qr.size[0]-49 and j<24) or ((i,j) in aligs) or (i%3==1 and j%3==1) or (bg0.getpixel((i,j))[3]==0)):
                    qr.putpixel((i+12,j+12), bg.getpixel((i,j)))

        qr_name = os.path.join(save_dir, os.path.splitext(os.path.basename(bg_name))[0] + '_qrcode.png') if not save_name else os.path.join(save_dir, save_name)
        qr.resize((qr.size[0]*3, qr.size[1]*3)).save(qr_name)
        return qr_name
    
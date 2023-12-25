#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from amzqr.mylibs import theqrmodule
from PIL import Image

"""

考慮將 /mylibs/theqrmodule.py 合併過來
並將 /mylibs/theqrmodule.py 移除

"""
   
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

from dataclasses import dataclass

@dataclass
class QRCodeConfig:
    words: str
    version: int = 1
    level: str = 'H'
    picture: str = None
    colorized: bool = False
    contrast: float = 1.0
    brightness: float = 1.0
    save_name: str = None
    save_dir: str = os.getcwd()

    def __post_init__(self): # 實例初始化後被呼叫
        self.check()

    def check(self):
        supported_chars = r"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ··,.:;+-*/\~!@#$%^&`'=<>[]()?_{}|"

        # check every parameter
        if not isinstance(self.words, str) or any(i not in supported_chars for i in self.words):
            raise ValueError('Wrong words! Make sure the characters are supported!')
        if not isinstance(self.version, int) or self.version not in range(1, 41):
            raise ValueError('Wrong version! Please choose a int-type value from 1 to 40!')
        if not isinstance(self.level, str) or len(self.level)>1 or self.level not in 'LMQH':
            raise ValueError("Wrong level! Please choose a str-type level from {'L','M','Q','H'}!")
        if self.picture:
            if not isinstance(self.picture, str) or not os.path.isfile(self.picture) or self.picture[-4:] not in ('.jpg','.png','.bmp','.gif'):
                raise ValueError("Wrong picture! Input a filename that exists and be tailed with one of {'.jpg', '.png', '.bmp', '.gif'}!")
            if self.picture[-4:] == '.gif' and self.save_name and self.save_name[-4:] != '.gif':
                raise ValueError('Wrong save_name! If the picuter is .gif format, the output filename should be .gif format, too!')
            if not isinstance(self.colorized, bool):
                raise ValueError('Wrong colorized! Input a bool-type value!')
            if not isinstance(self.contrast, float):
                raise ValueError('Wrong contrast! Input a float-type value!')
            if not isinstance(self.brightness, float):
                raise ValueError('Wrong brightness! Input a float-type value!')
        if self.save_name and (not isinstance(self.save_name, str) or self.save_name[-4:] not in ('.jpg','.png','.bmp','.gif')):
            raise ValueError("Wrong save_name! Input a filename tailed with one of {'.jpg', '.png', '.bmp', '.gif'}!")
        if not os.path.isdir(self.save_dir):
            raise ValueError('Wrong save_dir! Input a existing-directory!')

class QRStarter:
    def __init__(self, params: QRCodeConfig):
        self.params = params # QRParams

    # 組合 QR 碼與背景圖片(有指定背景圖片才會用到)
    def combine(self, ver, qr_name, bg_name, colorized, contrast, brightness, save_dir, save_name=None):
        from amzqr.mylibs.constant import alig_location
        from PIL import ImageEnhance, ImageFilter

        # 打開 QR 碼圖片，並根據 colorized 參數決定是否轉換為 RGBA 模式
        qr = Image.open(qr_name)
        qr = qr.convert('RGBA') if colorized else qr
        # 打開背景圖片，並轉換為 RGBA 模式
        bg0 = Image.open(bg_name).convert('RGBA')
        # 調整背景圖片的對比度和亮度
        bg0 = ImageEnhance.Contrast(bg0).enhance(contrast)
        bg0 = ImageEnhance.Brightness(bg0).enhance(brightness)

        # 調整背景圖片的大小以適應 QR 碼圖片的大小
        # 24 可能代表了 QR 碼圖像周圍的邊距或空白區域的大小
        if bg0.size[0] < bg0.size[1]:
            bg0 = bg0.resize((qr.size[0]-24, (qr.size[0]-24)*int(bg0.size[1]/bg0.size[0])))
        else:
            bg0 = bg0.resize(((qr.size[1]-24)*int(bg0.size[0]/bg0.size[1]), qr.size[1]-24))    
        
        # 如果 colorized 為 False，將背景圖片轉換為 1 位色模式(黑白圖)
        bg = bg0 if colorized else bg0.convert('1')
        
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

        # 將背景圖片與 QR 碼圖片結合
        for i in range(qr.size[0]-24):
            for j in range(qr.size[1]-24):
                if not ((i in (18,19,20)) or (j in (18,19,20)) or (i<24 and j<24) or (i<24 and j>qr.size[1]-49) or (i>qr.size[0]-49 and j<24) or ((i,j) in aligs) or (i%3==1 and j%3==1) or (bg0.getpixel((i,j))[3]==0)):
                    qr.putpixel((i+12,j+12), bg.getpixel((i,j)))
        
        # 保存結合後的圖片，並回傳圖片名
        qr_name = os.path.join(save_dir, os.path.splitext(os.path.basename(bg_name))[0] + '_qrcode.png') if not save_name else os.path.join(save_dir, save_name)
        qr.resize((qr.size[0]*3, qr.size[1]*3)).save(qr_name)
        return qr_name

    def _


    def run(self):        
        tempdir = os.path.join(os.path.expanduser('~'), '.myqr') # 創建暫時資料夾
        
        # 生成 QR 碼，處理圖片，並保存最終結果
        try:
            if not os.path.exists(tempdir):
                os.makedirs(tempdir)

            ver, qr_name = theqrmodule.get_qrcode(self.params.version, self.params.level, self.params.words, tempdir)

            if self.params.picture and self.params.picture[-4:]=='.gif':
                import imageio
                
                im = Image.open(picture)
                duration = im.info.get('duration', 0) # 獲取持續時間，如果沒有找到持續時間信息，則默認為 0
                print("duration : ", duration)

                # 將 GIF 的每幀保存為單獨的 PNG 文件
                im.save(os.path.join(tempdir, '0.png'))
                while True:
                    try:
                        seq = im.tell() # 返回當前幀的索引
                        im.seek(seq + 1)
                        im.save(os.path.join(tempdir, '%s.png' %(seq+1)))
                    except EOFError: # 達文件末尾
                        break
                
                # 為每幀生成 QR 碼並保存路徑
                imsname = []
                for s in range(seq+1):
                    bg_name = os.path.join(tempdir, '%s.png' % s)
                    imsname.append(combine(ver, qr_name, bg_name, colorized, contrast, brightness, tempdir))
                # ims = [imageio.imread(pic) for pic in imsname]
                ims = [Image.open(pic) if colorized else Image.open(pic).convert('L') for pic in imsname] # 當 colorized 為預設的 False，便將每張圖轉為灰度圖(0~255)

                qr_name = os.path.join(save_dir, os.path.splitext(os.path.basename(picture))[0] + '_qrcode.gif') if not save_name else os.path.join(save_dir, save_name)
                # imageio.mimwrite(qr_name, ims, '.gif', **{ 'duration': duration/1000 })
                imageio.mimwrite(qr_name, ims, '.gif', **{ 'duration': duration, 'loop': 0 }) # 處理為原速播放，並設置為循環播放的 gif
            elif self.params.picture:
                qr_name = combine(ver, qr_name, picture, colorized, contrast, brightness, save_dir, save_name)
            elif qr_name:
                qr = Image.open(qr_name)
                qr_name = os.path.join(save_dir, os.path.basename(qr_name)) if not save_name else os.path.join(save_dir, save_name)
                qr.resize((qr.size[0]*3, qr.size[1]*3)).save(qr_name)
            return ver, self.params.level, qr_name
            
        except:
            raise
        # 處理臨時目錄和文件的清理
        finally:
            import shutil
            if os.path.exists(tempdir):
                shutil.rmtree(tempdir) 



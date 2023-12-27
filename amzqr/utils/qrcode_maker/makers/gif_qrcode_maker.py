from amzqr.utils.qrcode_config import QRCodeConfig
from ..base_qrcode_maker import BaseQRCodeMaker
from typing import Tuple
from PIL import Image
import os

class GIFQRCodeMaker(BaseQRCodeMaker):
    def __init__(self, params: QRCodeConfig):
        super().__init__(params)

    # override
    def run(self):
        tempdir = self._make_tempdir()
        try:
            new_ver, qr_name = self._get_qrcode(tempdir)

            import imageio
            im = Image.open(self.params.picture)
            duration = im.info.get('duration', 0) # 獲取持續時間，如果沒有找到持續時間信息，則默認為 0
            print("duration : ", duration)

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
                imsname.append(self._combine(new_ver, qr_name, bg_name, tempdir))
            # ims = [imageio.imread(pic) for pic in imsname]
            ims = [Image.open(pic) if self.params.colorized else Image.open(pic).convert('L') for pic in imsname] # 當 colorized 為預設的 False，便將每張圖轉為灰度圖(0~255)

            qr_name = os.path.join(self.params.save_dir, os.path.splitext(os.path.basename(self.params.picture))[0] + '_qrcode.gif') if not self.params.save_name else os.path.join(self.params.save_dir, self.params.save_name)
            # imageio.mimwrite(qr_name, ims, '.gif', **{ 'duration': duration/1000 })
            imageio.mimwrite(qr_name, ims, '.gif', **{ 'duration': duration, 'loop': 0 }) # 處理為原速播放，並設置為循環播放的 gif
            return new_ver, self.params.level, qr_name
        except:
            raise
        finally:
            import shutil
            if os.path.exists(tempdir):
                shutil.rmtree(tempdir) 


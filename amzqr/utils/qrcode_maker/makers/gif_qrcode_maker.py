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
            duration = im.info.get('duration', 0)

            im.save(os.path.join(tempdir, '0.png'))
            while True:
                try:
                    seq = im.tell()
                    im.seek(seq + 1)
                    im.save(os.path.join(tempdir, '%s.png' %(seq+1)))
                except EOFError:
                    break
            
            imsname = []
            for s in range(seq+1):
                bg_name = os.path.join(tempdir, '%s.png' % s)
                imsname.append(self._combine(new_ver, qr_name, bg_name, tempdir))
            ims = [Image.open(pic) if self.params.colorized else Image.open(pic).convert('L') for pic in imsname]

            qr_name = os.path.join(self.params.save_dir, os.path.splitext(os.path.basename(self.params.picture))[0] + '_qrcode.gif') if not self.params.save_name else os.path.join(self.params.save_dir, self.params.save_name)
            imageio.mimwrite(qr_name, ims, '.gif', **{ 'duration': duration/1000, 'loop': 0 }) 
            return new_ver, self.params.level, qr_name
        except:
            raise
        finally:
            import shutil
            if os.path.exists(tempdir):
                shutil.rmtree(tempdir) 


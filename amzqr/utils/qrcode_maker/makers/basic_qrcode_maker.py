from amzqr.utils.qrcode_config import QRCodeConfig
from ..base_qrcode_maker import BaseQRCodeMaker
from typing import Tuple
from PIL import Image
import os

class BasicQRCodeMaker(BaseQRCodeMaker):
    def __init__(self, params: QRCodeConfig):
        super().__init__(params)

    # override
    def run(self):
        tempdir = self._make_tempdir()
        try:
            new_ver, qr_name = self._get_qrcode(tempdir)
            print(qr_name)
            qr = Image.open(qr_name)
            qr_name = os.path.join(self.params.save_dir, os.path.basename(qr_name)) if not self.params.save_name else os.path.join(self.params.save_dir, self.params.save_name)
            qr.resize((qr.size[0]*3, qr.size[1]*3)).save(qr_name)
            return new_ver, self.params.level, qr_name
        except:
            raise FileNotFoundError("qr_name not exist")
        finally:
            import shutil
            if os.path.exists(tempdir):
                shutil.rmtree(tempdir) 
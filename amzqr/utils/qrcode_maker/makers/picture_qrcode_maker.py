from amzqr.utils.qrcode_config import QRCodeConfig
from ..base_qrcode_maker import BaseQRCodeMaker
import os

class PictureQRCodeMaker(BaseQRCodeMaker):
    def __init__(self, params: QRCodeConfig):
        super().__init__(params)

    # override
    def run(self):
        tempdir = self._make_tempdir()
        try:
            new_ver, qr_name = self._get_qrcode(tempdir)
            qr_name = self._combine(new_ver, qr_name, self.params.picture, self.params.save_name)
            return new_ver, self.params.level, qr_name
        except:
            raise
        finally:
            import shutil
            if os.path.exists(tempdir):
                shutil.rmtree(tempdir)
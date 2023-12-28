from .makers.basic_qrcode_maker import BasicQRCodeMaker
from .makers.picture_qrcode_maker import PictureQRCodeMaker
from .makers.gif_qrcode_maker import GIFQRCodeMaker

from .base_qrcode_maker import BaseQRCodeMaker
from amzqr.mylibs.qrcode_config import QRCodeConfig

class QRCodeMakerFactory:
    @staticmethod
    def get_maker(params: QRCodeConfig) -> BaseQRCodeMaker:
        if params.picture and params.picture[-4:]=='.gif':
            return GIFQRCodeMaker(params)
        elif params.picture:
            return PictureQRCodeMaker(params)
        else:
            return BasicQRCodeMaker(params)
        
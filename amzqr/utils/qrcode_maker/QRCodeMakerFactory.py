from .makers import BasicQRCodeMaker, PictureQRCodeMaker, GIFQRCodeMaker
from .BaseQRCodeMaker import BaseQRCodeMaker
from amzqr.utils.QRCodeConfig import QRCodeConfig

class QRCodeMakerFactory:
    @staticmethod
    def get_maker(params: QRCodeConfig) -> BaseQRCodeMaker:
        if params.picture and params.picture[-4:]=='.gif':
            return GIFQRCodeMaker(params)
        elif params.picture:
            return PictureQRCodeMaker(params)
        else:
            return BasicQRCodeMaker(params)
        
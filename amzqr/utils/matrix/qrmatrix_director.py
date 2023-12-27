from .basic_qrmatrix_builder import BasicQRMatrixBuilder

class QRMatrixDirector:
    def __init__(self):
        self.builder = BasicQRMatrixBuilder()

    def _construct(self, ver, ecl, bits):
        self.builder.reset(ver, ecl, bits)
        self.builder.add_finder_and_separator()
        self.builder.add_alignment()
        self.builder.add_timing()
        self.builder.add_dark_and_reserving()
        self.builder.make_maskmatrix()
        self.builder.place_bits()
        mask_num = self.builder.mask()
        self.builder.add_format_and_version_string(mask_num)

    def get_qrmatrix(self, ver, ecl, bits):
        self._construct(ver, ecl, bits)
        return self.builder.get_qrmatrix()
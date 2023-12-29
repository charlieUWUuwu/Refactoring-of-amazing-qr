import abc

class QRMatrixBuilder(abc.ABC):
    def reset(self, ver, ecl, bits):
        self.ver = ver
        self.ecl = ecl
        self.bits = bits

        self.mask_num = None
        self._maskmatrix = None

        num = (ver - 1) * 4 + 21
        self.qrmatrix =  [[None] * num for i in range(num)]

    @abc.abstractmethod
    def add_finder_and_separator(self):
        pass

    @abc.abstractmethod
    def add_alignment(self):
        pass

    @abc.abstractmethod
    def add_timing(self):
        pass

    @abc.abstractmethod
    def add_dark_and_reserving(self):
        pass

    @abc.abstractmethod
    def make_maskmatrix(self):
        pass

    @abc.abstractmethod
    def place_bits(self):
        pass

    @abc.abstractmethod
    def mask(self):
        pass

    @abc.abstractmethod
    def add_format_and_version_string(self, mask_num):
        pass

    def get_qrmatrix(self):
        return self.qrmatrix
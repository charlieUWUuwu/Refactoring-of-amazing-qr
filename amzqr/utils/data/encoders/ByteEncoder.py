from amzqr.utils.constant import alphanum_list
from ..BaseEncoder import BaseEncoder

class ByteEncoder(BaseEncoder):
    def __init__(self, ver, ecl):
        super().__init__(ver, ecl, mode='byte')

    def _get_code(self, str):
        code = ''
        for i in str:
            c = bin(ord(i.encode('iso-8859-1')))[2:]
            c = '0'*(8-len(c)) + c
            code += c
        return code

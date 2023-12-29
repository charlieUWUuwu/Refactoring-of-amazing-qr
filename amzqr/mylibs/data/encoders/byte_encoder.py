from ..base_encoder import BaseEncoder

class ByteEncoder(BaseEncoder):
    def __init__(self, ver, ecl):
        super().__init__(ver, ecl, mode='byte')

    def get_code(self, str):
        code = ''
        for i in str:
            c = bin(ord(i.encode('iso-8859-1')))[2:]
            c = '0'*(8-len(c)) + c
            code += c
        return code

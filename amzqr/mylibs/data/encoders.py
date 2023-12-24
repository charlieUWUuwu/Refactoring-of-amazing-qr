from amzqr.mylibs.constant import alphanum_list
from .base_encoder import base_encoder

class NumericEncoder(base_encoder):
    def __init__(self, ver, ecl):
        super().__init__(ver, ecl, mode='numeric')

    def _get_code(self, str):
        str_list = [str[i:i+3] for i in range(0,len(str),3)]
        code = ''
        for i in str_list:
            rqbin_len = 10
            if len(i) == 1: 
                rqbin_len = 4
            elif len(i) == 2:
                rqbin_len = 7
            code_temp = bin(int(i))[2:]
            code += ('0'*(rqbin_len - len(code_temp)) + code_temp)
        return code

class AlphanumericEncoder(base_encoder):
    def __init__(self, ver, ecl):
        super().__init__(ver, ecl, mode='alphanumeric')

    def _get_code(self, str):
        code_list = [alphanum_list.index(i) for i in str]
        code = ''
        for i in range(1, len(code_list), 2):
            c = bin(code_list[i-1] * 45 + code_list[i])[2:]
            c = '0'*(11-len(c)) + c
            code += c
        if i != len(code_list) - 1:
            c = bin(code_list[-1])[2:]
            c = '0'*(6-len(c)) + c
            code += c
        return code
    
class KanjiEncoder(base_encoder):
    def __init__(self, ver, ecl):
        super().__init__(ver, ecl, mode='kanji')

    def _get_code(self, str):
        pass

class ByteEncoder(base_encoder):
    def __init__(self, ver, ecl):
        super().__init__(ver, ecl, mode='byte')

    def _get_code(self, str):
        code = ''
        for i in str:
            c = bin(ord(i.encode('iso-8859-1')))[2:]
            c = '0'*(8-len(c)) + c
            code += c
        return code

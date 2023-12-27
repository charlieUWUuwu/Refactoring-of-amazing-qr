from amzqr.utils.constant import alphanum_list
from ..BaseEncoder import BaseEncoder

class AlphanumericEncoder(BaseEncoder):
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
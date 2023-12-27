from ..base_encoder import BaseEncoder

class NumericEncoder(BaseEncoder):
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
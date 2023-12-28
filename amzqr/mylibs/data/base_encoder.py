from amzqr.mylibs.constant import required_bytes, mindex, lindex, grouping_list, mode_indicator
import abc
from typing import Any

# ecl: Error Correction Level(L,M,Q,H)

class BaseEncoder(abc.ABC):
    def __init__(self, ver, ecl, mode=None):
        self.ver = ver
        self.ecl = ecl
        self.mode = mode # 繼承的 class 有各自指定

    @abc.abstractmethod
    def _get_code(self, str) -> Any: 
        raise NotImplementedError

    def _get_cci(self, str) -> str:
        if self.mode is None:
            raise TypeError("Mode is not set to a valid type.")
        
        if 1 <= self.ver <= 9:
            cci_len = (10, 9, 8, 8)[mindex[self.mode]]
        elif 10 <= self.ver <= 26:
            cci_len = (12, 11, 16, 10)[mindex[self.mode]]
        else:
            cci_len = (14, 13, 16, 12)[mindex[self.mode]]
            
        cci = bin(len(str))[2:]
        cci = '0' * (cci_len - len(cci)) + cci
        return cci

    def encode(self, str):
        code = mode_indicator[self.mode] + self._get_cci(str) + self._get_code(str)
        
        # Add a Terminator
        rqbits = 8 * required_bytes[self.ver-1][lindex[self.ecl]]
        b = rqbits - len(code)
        code += '0000' if b >= 4 else '0' * b
        
        # Make the Length a Multiple of 8
        while len(code) % 8 != 0:
            code += '0'
        
        # Add Pad Bytes if the String is Still too Short
        while len(code) < rqbits:    
            code += '1110110000010001' if rqbits - len(code) >= 16 else '11101100'
            
        data_code = [code[i:i+8] for i in range(len(code)) if i%8 == 0]
        data_code = [int(i,2) for i in data_code]

        g = grouping_list[self.ver-1][lindex[self.ecl]]
        data_codewords, i = [], 0
        for n in range(g[0]):
            data_codewords.append(data_code[i:i+g[1]])
            i += g[1]
        for n in range(g[2]):
            data_codewords.append(data_code[i:i+g[3]])
            i += g[3]
        
        return self.ver, data_codewords
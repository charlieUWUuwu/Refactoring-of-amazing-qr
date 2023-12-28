from amzqr.mylibs.constant import char_cap, mindex, num_list, alphanum_list

from .encoders.byte_encoder import ByteEncoder
from .encoders.kanji_encoder import KanjiEncoder
from .encoders.numeric_encoder import NumericEncoder
from .encoders.alphanumeric_encoder import AlphanumericEncoder


class EncoderFactory:
    @staticmethod
    def get_encoder(ver, ecl, str):
        new_ver, mode = analyse(ver, ecl, str)  # Determine the mode based on data
        print('line 16: mode:', mode)

        if mode == 'numeric':
            return NumericEncoder(new_ver, ecl)
        elif mode == 'alphanumeric':
            return AlphanumericEncoder(new_ver, ecl)
        elif mode == 'byte':
            return ByteEncoder(new_ver, ecl)
        elif mode == 'kanji':
            return KanjiEncoder(new_ver, ecl)
        else:
            raise ValueError("Unsupported mode determined by analysis")
        
        
# 根據 str 分析種類
def analyse(ver, ecl, str):
    new_ver = ver
    if all(i in num_list for i in str):
        mode = 'numeric'
    elif all(i in alphanum_list for i in str):
        mode = 'alphanumeric'
    else:
        mode = 'byte'
    
    m = mindex[mode]
    l = len(str)
    for i in range(40):
        if char_cap[ecl][i][m] > l:
            new_ver = i + 1 if i+1 > new_ver else new_ver
            break
    return new_ver, mode
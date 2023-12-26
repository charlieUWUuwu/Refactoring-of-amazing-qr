from amzqr.utils.constant import char_cap, mindex, num_list, alphanum_list
from .encoders import ByteEncoder, KanjiEncoder, NumericEncoder, AlphanumericEncoder

class QRCodeEncoderFactory:
    @staticmethod
    def get_encoder(ver, ecl, str):
        ver, mode = analyse(ver, ecl, str)  # Determine the mode based on data
        print('line 16: mode:', mode)

        if mode == 'numeric':
            return NumericEncoder(ver, ecl)
        elif mode == 'alphanumeric':
            return AlphanumericEncoder(ver, ecl)
        elif mode == 'byte':
            return ByteEncoder(ver, ecl)
        elif mode == 'kanji':
            return KanjiEncoder(ver, ecl)
        else:
            raise ValueError("Unsupported mode determined by analysis")
        
        
# 根據 str 分析種類
def analyse(ver, ecl, str):
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
            ver = i + 1 if i+1 > ver else ver
            break
    return ver, mode
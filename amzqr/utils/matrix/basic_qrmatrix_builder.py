from amzqr.utils.constant import alig_location, format_info_str, version_info_str, lindex
from .evaluations import Scorer
from .qrmatrix_builder import QRMatrixBuilder

# 具體實現
class BasicQRMatrixBuilder(QRMatrixBuilder):
    # override
    def add_finder_and_separator(self):
        m = self.qrmatrix.copy()
        for i in range(8):
            for j in range(8):
                if i in (0, 6):
                    m[i][j] = m[-i-1][j] = m[i][-j-1] = 0 if j == 7 else 1
                elif i in (1, 5):
                    m[i][j] = m[-i-1][j] = m[i][-j-1] = 1 if j in (0, 6) else 0  
                elif i == 7:
                    m[i][j] = m[-i-1][j] = m[i][-j-1] = 0
                else:
                    m[i][j] = m[-i-1][j] = m[i][-j-1] = 0 if j in (1, 5, 7) else 1
        self.qrmatrix = m

    # override
    def add_alignment(self):
        def add_an_alignment(row, column, m):
            for i in range(row-2, row+3):
                for j in range(column-2, column+3):
                    m[i][j] = 1 if i in (row-2, row+2) or j in (column-2, column+2) else 0
            m[row][column] = 1

        m = self.qrmatrix.copy()
        if self.ver > 1:
            coordinates = alig_location[self.ver-2]
            for i in coordinates:
                for j in coordinates:
                    if m[i][j] is None:
                        add_an_alignment(i, j, m)
        self.qrmatrix = m

    # override
    def add_timing(self):
        for i in range(8, len(self.qrmatrix)-8):
            self.qrmatrix[i][6] = self.qrmatrix[6][i] = 1 if i % 2 ==0 else 0

    # override
    def add_dark_and_reserving(self):
        m = self.qrmatrix.copy()
        for j in range(8):
            m[8][j] = m[8][-j-1] = m[j][8] = m[-j-1][8] = 0
        m[8][8] = 0
        m[8][6] = m[6][8] = m[-8][8] = 1
        
        if self.ver > 6:
            for i in range(6):
                for j in (-9, -10, -11):
                    m[i][j] = m[j][i] = 0
        self.qrmatrix = m

    # override
    def make_maskmatrix(self):
        self.maskmatrix = [i[:] for i in self.qrmatrix]

    # override
    def place_bits(self):
        bit = (int(i) for i in self.bits)
        m = self.qrmatrix.copy()

        up = True
        for a in range(len(m)-1, 0, -2):
            a = a-1 if a <= 6 else a
            irange = range(len(m)-1, -1, -1) if up else range(len(m))
            for i in irange:
                for j in (a, a-1):
                    if m[i][j] is None:
                        m[i][j] = next(bit)
            up = not up
        self.qrmatrix = m

    # override
    def mask(self):
        mps = get_mask_patterns(self.maskmatrix)
        scores = []
        for mp in mps:
            for i in range(len(mp)):
                for j in range(len(mp)):
                    mp[i][j] = mp[i][j] ^ self.qrmatrix[i][j]
            scores.append(Scorer.compute_score(mp))
        best = scores.index(min(scores))
        self.qrmatrix = mps[best]
        return best

    # override
    def add_format_and_version_string(self, mask_num):
        m = self.qrmatrix.copy()
        fs = [int(i) for i in format_info_str[lindex[self.ecl]][mask_num]]
        for j in range(6):
            m[8][j] = m[-j-1][8] = fs[j]
            m[8][-j-1] = m[j][8] = fs[-j-1]
        m[8][7] = m[-7][8] = fs[6]
        m[8][8] = m[8][-8] = fs[7]
        m[7][8] = m[8][-7] = fs[8]
        
        if self.ver > 6:
            vs = (int(i) for i in version_info_str[self.ver-7])
            for j in range(5, -1, -1):
                for i in (-9, -10, -11):
                    m[i][j] = m[j][i] = next(vs)
        self.qrmatrix = m

def get_mask_patterns(mm):
    def formula(i, row, column):
        if i == 0:
            return (row + column) % 2 == 0
        elif i == 1:
            return row % 2 == 0
        elif i == 2:
            return column % 3 == 0
        elif i == 3:
            return (row + column) % 3 == 0
        elif i == 4:
            return (row // 2 + column // 3) % 2 == 0
        elif i == 5:
            return ((row * column) % 2) + ((row * column) % 3) == 0
        elif i == 6:
            return (((row * column) % 2) + ((row * column) % 3)) % 2 == 0
        elif i == 7:
            return 	(((row + column) % 2) + ((row * column) % 3)) % 2 == 0

    mm[-8][8] = None
    for i in range(len(mm)):
        for j in range(len(mm)):
            mm[i][j] = 0 if mm[i][j] is not None else mm[i][j]
    mps = []
    for i in range(8):
        mp = [ii[:] for ii in mm]
        for row in range(len(mp)):
            for column in range(len(mp)):
                mp[row][column] = 1 if mp[row][column] is None and formula(i, row, column) else 0
        mps.append(mp)
        
    return mps
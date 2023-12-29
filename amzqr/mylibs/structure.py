# -*- coding: utf-8 -*-

from amzqr.mylibs.constant import required_remainder_bits, lindex, grouping_list

class Structure:
    def structure_final_bits(self, ver, ecl, data_codewords, ecc):
        final_message = self._interleave_dc(ver, ecl, data_codewords) + self._interleave_ecc(ecc)
        
        # convert to binary & Add Remainder Bits if Necessary
        final_bits = ''.join(['0'*(8-len(i))+i for i in [bin(i)[2:] for i in final_message]]) + '0' * required_remainder_bits[ver-1]
        
        return final_bits

    def _interleave_dc(self, ver, ecl, data_codewords):
        id = []
        for t in zip(*data_codewords):
            id += list(t)
        g = grouping_list[ver-1][lindex[ecl]]
        if g[3]:
            for i in range(g[2]):
                id.append(data_codewords[i-g[2]][-1])
        return id
        
    def _interleave_ecc(self, ecc):
        ie = []
        for t in zip(*ecc):
            ie += list(t)
        return ie
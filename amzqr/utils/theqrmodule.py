# -*- coding: utf-8 -*-

from amzqr.utils import structure
from amzqr.utils.ECC import ECC
from amzqr.utils.data.encoder_factory import EncoderFactory
from amzqr.utils.draw.qrcode_drawer import QRCodeDrawer
from amzqr.utils.matrix.qrmatrix_director import QRMatrixDirector

# ver: Version from 1 to 40
# ecl: Error Correction Level (L,M,Q,H)
# str: words
# get a qrcode picture of 3*3 pixels per module
def get_qrcode(ver, ecl, str, save_place):
    # Data Coding
    # ver, data_codewords = data.encode(ver, ecl, str)
    encoder = EncoderFactory.get_encoder(ver, ecl, str)
    new_ver, data_codewords = encoder.encode(str)

    # Error Correction Coding
    ecc = ECC.encode(new_ver, ecl, data_codewords)
    
    # Structure final bits
    final_bits = structure.structure_final_bits(new_ver, ecl, data_codewords, ecc)
    
    # Get the QR Matrix
    director = QRMatrixDirector()
    qrmatrix = director.get_qrmatrix(new_ver, ecl, final_bits)
    # qrmatrix = matrix.get_qrmatrix(new_ver, ecl, final_bits)
        
    # Draw the picture and Save it, then return the real ver and the absolute name
    return new_ver, QRCodeDrawer.draw_qrcode(save_place, qrmatrix)


# -*- coding: utf-8 -*-

from amzqr.mylibs import ECC, structure, draw
from amzqr.mylibs.data.QRCodeEncoderFactory import QRCodeEncoderFactory
from amzqr.mylibs.matrix.QRMatrixDirector import QRMatrixDirector

# ver: Version from 1 to 40
# ecl: Error Correction Level (L,M,Q,H)
# str: words
# get a qrcode picture of 3*3 pixels per module
def get_qrcode(ver, ecl, str, save_place):
    # Data Coding
    # ver, data_codewords = data.encode(ver, ecl, str)
    encoder = QRCodeEncoderFactory.get_encoder(ver, ecl, str)
    ver, data_codewords = encoder.encode(str)

    # Error Correction Coding
    ecc = ECC.encode(ver, ecl, data_codewords)
    
    # Structure final bits
    final_bits = structure.structure_final_bits(ver, ecl, data_codewords, ecc)
    
    # Get the QR Matrix
    director = QRMatrixDirector()
    qrmatrix = director.get_qrmatrix(ver, ecl, final_bits)
    # qrmatrix = matrix.get_qrmatrix(ver, ecl, final_bits)
        
    # Draw the picture and Save it, then return the real ver and the absolute name
    return ver, draw.draw_qrcode(save_place, qrmatrix)


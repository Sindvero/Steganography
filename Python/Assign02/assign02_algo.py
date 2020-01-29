import binascii


def str2bin(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:] # Transform the text in binary code with the correct
                                                                         # enoding (I had issue with it so I force utf-8) and
                                                                         # remove "0b" from the transformation thanks to [2:]
                                                                         # librarie:http://www.pythonlake.com/int-from_bytes
    
    return bits.zfill(8 * ((len(bits) + 7) // 8)) # each ASCII character is 8 bits



print(str2bin("AAAA\n"))
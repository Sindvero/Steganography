import binascii


def str2bin(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:] # Transform the text in binary code with the correct
                                                                         # enoding (I had issue with it so I force utf-8) and
                                                                         # remove "0b" from the transformation thanks to [2:]
                                                                         # librarie:http://www.pythonlake.com/int-from_bytes
    
    return bits.zfill(8 * ((len(bits) + 7) // 8)) # each ASCII character is 8 bits


# Open both input and output file
fp = open("Python/Assign02/output_file.txt", "a")
fp_declaration_of_independant = open("Python/Assign02/Declaration_of_Independence.txt", "r")

# Store input text in a string buffer
buffer = fp_declaration_of_independant.read()

# Close input file
fp_declaration_of_independant.close()

# Transform ASCII char into binary and store them within a text file
fp.write(str2bin(buffer))
fp.close()
print(str2bin(buffer))
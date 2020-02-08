import binascii


def str2bin(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:] # Transform the text in binary code with the correct
                                                                         # encoding (I had issue with it so I force utf-8) and
                                                                         # remove "0b" from the transformation thanks to [2:]
                                                                         # librarie:http://www.pythonlake.com/int-from_bytes
    
    return bits.zfill(8 * ((len(bits) + 7) // 8)) # each ASCII character is 8 bits

def bin2str(text, encoding='utf-8', errors='surrogatepass'):
    n = int(text, 2)

    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding,errors) or '\0'


###################################
#   Transformation Text to Binary
###################################

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

###################################
#   Transformation Binary to Text
###################################

# Open both binay file and output file
fp_bin_file = open("Python/Assign02/output_file.txt", "r")
fp_declaration_of_independant_from_bit = open("Python/Assign02/test_return.txt", "a")

# Store Binary in a string buffer
buffer_bin = fp_bin_file.read()

# Close input file 
fp_bin_file.close()

# Transform bits into ASCII char and store the text within a text file
fp_declaration_of_independant_from_bit.write(bin2str(buffer_bin))
fp_declaration_of_independant_from_bit.close()
print(bin2str(buffer_bin) + '\n')

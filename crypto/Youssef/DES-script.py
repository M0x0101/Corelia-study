#initial permutation table
IP=[  58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

def permute(block, table):
    permuted_block = []
    for x in table:
        permuted_block.append(block[x - 1])
    return permuted_block

def initial_permutation(block):
    return permute(block, IP)

# key generation

# parity drop table
PD=[   57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

# shift Algorithm        
shift_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2]

# Compression P-Box
compression = [
        14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32 ]

def shifting(block, n):
    return block[n:] + block[:n]
      
def key_generate(key):
    key = permute(key, PD) # parity drop for key to make it 56 bits
    left, right = key[:28], key[28:] # split the key into two halves
    subkeys = []
    for shift in shift_table:
        left = shifting(left, shift) #shifting into left side 
        right = shifting(right, shift)
        combine = left + right
        subkeys.append(permute(combine, compression))
    return subkeys    
    
# F-function
expansion = [32, 1, 2, 3, 4, 5,  # Expansion P-Box
             4, 5, 6, 7, 8, 9,
             8, 9, 10, 11, 12, 13,
             12, 13, 14, 15, 16, 17,
             16, 17, 18, 19, 20, 21,
             20, 21, 22, 23, 24, 25,
             24, 25, 26, 27, 28, 29,
             28, 29, 30, 31, 32, 1]

SBOX = [
    # S1
    [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
     [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
     [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
     [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],
    # S2
    [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
     [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
     [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
     [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],
    # S3
    [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
     [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
     [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
     [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],
    # S4
    [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
     [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
     [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
     [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],
    # S5
    [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
     [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
     [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
     [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],
    # S6
    [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
     [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
     [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
     [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],
    # S7
    [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
     [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
     [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
     [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],
    # S8
    [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
     [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
     [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
     [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
]

straight = [ # straight P-Box
     16, 7, 20, 21,
     29, 12, 28, 17,
     1, 15, 23, 26,
     5, 18, 31, 10,
     2, 8, 24, 14,
     32, 27, 3, 9,
     19, 13, 30, 6,
     22, 11, 4, 25]

def xor(b1, b2):
    return [a ^ b for a, b in zip(b1, b2)]
    
def sbox_substitution(block):
    sub_blocks = [block[i:i+6] for i in range(0, 48, 6)]
    result = []
    for i, sub_block in enumerate(sub_blocks):
        row = (sub_block[0] << 1) + sub_block[5]
        col = (sub_block[1] << 3) + (sub_block[2] << 2) + (sub_block[3] << 1) + sub_block[4]
        result += [int(bit) for bit in bin(SBOX[i][row][col])[2:].zfill(4)]
    return result

def F_function(right, subkey):
    right_expansion = permute(right, expansion)
    xored = xor(right_expansion, subkey)
    SBox_process = sbox_substitution(xored)
    return permute(SBox_process, straight)

def round(left, right, subkey):
    right_result = xor(left, F_function(right, subkey))
    return right, right_result
    
def des_block(block, subkeys):
    block = initial_permutation(block)
    left, right = block[:32], block[32:]
    for i in range(16):
        left, right = round(left, right, subkeys[i])
        combine = left + right
    return final_permutation(combine)

# Final Permutation
FP = [40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41, 9, 49, 17, 57, 25]

def final_permutation(block):
    return permute(block, FP)

# Encryption Function
def des_encryption(block, key):
    subkeys = key_generate(key)
    return des_block(block, subkeys)

# Convert input to binary
def hex_to_bin(hex_str):
    return [int(bit) for bit in bin(int(hex_str, 16))[2:].zfill(64)]

# convert result to hex
def bin_to_hex(bin_list):
    return hex(int(''.join(map(str, bin_list)), 2))[2:].zfill(16)

def main():
    plaintext = "0123456789ABCDEF"
    key = "133457799BBCDFF1"
    plaintext_bin = hex_to_bin(plaintext)
    key_bin = hex_to_bin(key)
    
    ciphertext_bin = des_encryption(plaintext_bin, key_bin)
    ciphertext = bin_to_hex(ciphertext_bin)
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print(f"Ciphertext: {ciphertext}")

if __name__ == "__main__":
    main()
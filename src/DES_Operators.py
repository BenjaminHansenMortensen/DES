import Operators
import Tables
import Formater

# Initial vector given
iv = [0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0,
      1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0]


def encryptor(plaintext, subkeys):
    bit_plaintext = Formater.text_to_8bit_list(plaintext)
    padded_amount = Operators.calculate_padding(bit_plaintext) # Calculates padding to apply on the last block
    bit_plaintext = Operators.add_padding(bit_plaintext) # Applies padding on the last block unless it is 64 bits

    encrypted_message = ""
    for k in range(0, Operators.amount_of_blocks(bit_plaintext)): # Takes all blocks and applies IV
        block = Operators.get_kth_block(bit_plaintext, k)

        global iv
        block = Operators.xor(iv, block)       # Applies IV XOR on block
        iv = block_encryptor(block, subkeys)   # Updates IV to new encrypted block

        encrypted_message += Formater.bit_list_to_string(iv) # Adds together all blocks to ciphertext
        
    return encrypted_message + Formater.dec_to_6bit_string(padded_amount) # Returns ciphertext with 6 extra bits for
    									  # for padded amount


def decryptor(ciphertext, subkeys):
    bit_ciphertext = Formater.bit_string_to_bit_list(ciphertext)
    padded_amount = Formater.bit_list_to_dec(bit_ciphertext[-6:])# Gets padded amount on the last block from last 6 bits
    del bit_ciphertext[-6:]                                      # Removes last six bits

    bit_plaintext = []
    for k in range(0, Operators.amount_of_blocks(ciphertext)):  # Takes all blocks and applies IV
        block = Operators.get_kth_block(bit_ciphertext, k)

        global iv
        bit_plaintext += Operators.xor(iv, block_encryptor(block, subkeys[:: -1])) # Applies IV XOR on decrypted block
        iv = block                                                                 # Updates IV to new XORed block

    Operators.remove_padding(bit_plaintext, padded_amount)  # Removed padded amount from last block
    return Formater.bit_list_to_text(bit_plaintext)   # Returns original plaintext


def block_encryptor(byte_plaintext, subkeys): #Standard DES encryption/decryption of a 64 bit block
    ip = Operators.permutor(Tables.IP_Table, byte_plaintext) # Initial Permutation
    left_ip, right_ip = ip[0:32], ip[32:64] # Left, Right partitioning

    for i in range(0, 16):
        right_ip_prime = Operators.permutor(Tables.E_BitSelection_Table, right_ip) # Expantion function on right copy
        right_ip_prime = Operators.xor(right_ip_prime, subkeys[i])                 # Subkey XOR
        right_ip_prime = Operators.substitutor(right_ip_prime)                     # S-box substitution
        right_ip_prime = Operators.permutor(Tables.P_Table, right_ip_prime)        # Permutation
        right_ip_prime = Operators.xor(left_ip, right_ip_prime)                    # Left, Right partition XOR

        left_ip = right_ip                                                         # New Left with IP
        right_ip = right_ip_prime                                                  # New Right with IP

    return Operators.permutor(Tables.IPInverse_Table, right_ip + left_ip) # Swaps left and right partition, and
                                                                          # inverses Initial Permutation

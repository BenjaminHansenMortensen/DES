# Source: https://csrc.nist.gov/csrc/media/publications/fips/46/3/archive/1999-10-25/documents/fips46-3.pdf#page=15
from time import sleep

import DES_Operators
import sys
import DES_Subkey_Generator
import Formater


def mainencryption(): # Main Encryption, runs ECB and CBC mode accordingly, reads and writes to specified files
    plaintext_file = open(sys.argv[2], "r")
    plaintext = plaintext_file.read()
    if len(plaintext) == 8:  # If plaintext is 64 bits, it runs in ECB mode
        encrypted_message = Formater.bit_list_to_string(DES_Operators.block_encryptor(Formater.text_to_8bit_list(plaintext), subkeys))
    else:                    # Else it runs in CBC
        encrypted_message = DES_Operators.encryptor(plaintext, subkeys)
    plaintext_file.close()

    ciphertext_file = open(sys.argv[3], "w")
    ciphertext_file.write(encrypted_message)
    ciphertext_file.close()


def maindecryption(): # Main Decryption, runs ECB and CBC mode accordingly, reads and writes to specified files
    ciphertext_file = open(sys.argv[2], "r")
    ciphertext = ciphertext_file.read()
    if len(ciphertext) == 64: # If plaintext is 64 bits, it runs in ECB mode
        decrypted_message = Formater.bit_list_to_text(DES_Operators.block_encryptor(Formater.bit_string_to_bit_list(ciphertext), subkeys[:: -1]))
    else:                     # Else it runs in CBC
        decrypted_message = DES_Operators.decryptor(ciphertext, subkeys)
    ciphertext_file.close()

    plaintext_file = open(sys.argv[3], "w")
    plaintext_file.write(decrypted_message)
    plaintext_file.close()


if __name__ == '__main__':
    key = input("Enter your eight character ASCII key: ")      # Takes key for encrypting/decrypting
    subkeys = list(DES_Subkey_Generator.generate_subkey(key))  # Generates subkeys for given key

    if sys.argv[1] == "encrypt":                               # Runs encryption or decryption accordingly to args
        mainencryption()
    elif sys.argv[1] == "decrypt":
        maindecryption()

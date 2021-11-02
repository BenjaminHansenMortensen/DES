import Tables
import Formater

S_Boxes = [Tables.S1_Table, Tables.S2_Table, Tables.S3_Table, Tables.S4_Table,
           Tables.S5_Table, Tables.S6_Table, Tables.S7_Table, Tables.S8_Table]


def substitutor(bit_list):  # Applies S-box substitution on bit list
    index = []

    for k in range(0, 8):
        row = Formater.row_in_dec(bit_list, k)  # First and last bit in the 6bit kth partition
        column = Formater.column_in_dec(bit_list, k)  # Sum n for first < n < last in the kth 6bit partition

        index += Formater.dec_to_4bit_list(S_Boxes[k][row][column])

    return index


def xor(value1, value2):  # XORs two bit lists
    return list(value1[x] ^ value2[x] for x in range(0, len(value1)))


def permutor(table, values):  # Permutes a list based on passed table
    return [values[i-1] for i in table]


def add_padding(values):  # Applies padding on a block based on calculated amount to achieve a full 64 bit block
    if len(values) % 64 != 0:
        for i in range(0, (64 - (len(values) % 64))):
            values.append(0)
    return values


def remove_padding(bit_plaintext, padded_amount): # Removes applied padding on a block based on calculated amount
    if padded_amount != 0:
        del bit_plaintext[-padded_amount:]


def left_shift(partition):        # Applies a left shift to a partition
    partition.append(partition.pop(0))
    return partition


def double_left_shift(partition): # Applies two left shifts to a partition
    return left_shift(left_shift(partition))


def get_kth_block(bit_list, k): # Finds kth 64 bit block in a bit list
    return bit_list[k * 64: k * 64 + 64]


def calculate_padding(text): # Calculates padding to apply to achieve a full 64 bit block
    return 64 - len(text) % 64 if len(text) % 64 > 0 else 0


def amount_of_blocks(arr): # Calculates how many 64 bit blocks are in a bit list (plaintext/ciphertext)
    return int(len(arr) / 64)

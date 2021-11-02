import Tables
import Operators


def generate_subkey(key):  # Subkey generator object
    byte_key = list(map(int, ''.join(format(ord(i), 'b').zfill(8) for i in key)))

    pc1 = Operators.permutor(Tables.PC1_Table, byte_key)
    left_pc1, right_pc1 = pc1[0:28], pc1[28:56]  # Partitions into left and right partition

    for i in range(1, 17):  # i identifies which sub-key is being generated
        if i in [1, 2, 9, 16]: # Identifies cases for only one left shift on partition
            yield Operators.permutor(Tables.PC2_Table, Operators.left_shift(left_pc1) +
                                     Operators.left_shift(right_pc1))
        else:                # Applies two left shifts on partitions
            yield Operators.permutor(Tables.PC2_Table, Operators.double_left_shift(left_pc1) +
                                     Operators.double_left_shift(right_pc1))


def get_subkeys(key): # Builds list with 16 subkeys derived from key
    return [(generate_subkey(key)[i] for i in range(16))]


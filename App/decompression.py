from compression import TAG

def lz77_decompression(user_input):
    Original_Data = ""

    if type(user_input) == str:
        tags = []
        if type(user_input) == str:
            for tag in user_input.split():
                tag = tag.strip('<>')
                position, length, symbol = tag.split(",")
                symbol = symbol.strip('" \' “” ‘’ ')
                tags.append((int(position), int(length), symbol))

        for position, length, symbol in tags:
            if position > 0:
                for _ in range(length):
                    Original_Data += Original_Data[-position]
            if symbol != None and symbol != "NULL" and symbol != "":
                Original_Data += symbol

    else:
        for tag in user_input:
            if tag.position > 0:
                for _ in range(tag.length):
                    Original_Data += Original_Data[-tag.position]
            if tag.offset != None and tag.offset != "NULL" and tag.offset != "":
                Original_Data += tag.offset

    return Original_Data




def load_binary_tags(file_path):
    bits = ""
    with open (file_path, "rb") as file:
        tagsAsBytes = file.read()
        numOfBytes = len(tagsAsBytes)

        for i in range(numOfBytes):
            byte = format(tagsAsBytes[i], "08b")
            bits += byte

    pos_bits = int(bits[0:6],2)
    len_bits = int(bits[6:12],2)
    padding = int(bits[12:16],2)

    tags = []

    for i in range(16, len(bits)-padding, pos_bits + len_bits + 8):
        position = int(bits[i:i + pos_bits], 2)
        length = int(bits[i + pos_bits:i + pos_bits + len_bits], 2)
        symbol_bits = bits[i + pos_bits + len_bits:i + pos_bits + len_bits + 8]
        symbol = chr(int(symbol_bits, 2)) if symbol_bits != "00000000" else None

        tags.append(TAG(position, length, symbol))

    return tags
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
        #-------------------------------------
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
def decompress_text():
    # tags input
    user_input = input("Enter Tags: ")
    tags = []
    for tag in user_input.split():
        tag = tag.strip('<>')
        position, length, symbol = tag.split(",")
        symbol = symbol.strip('" \' “” ‘’ ')
        tags.append((int(position), int(length), symbol))
    # ----------------

    Original_Data = ""

    for position, length, symbol in tags:
        if position > 0:
            for _ in range(length):
                Original_Data += Original_Data[-position]
        if symbol != None and symbol != "NULL" and symbol != "":
            Original_Data += symbol

    print(Original_Data)
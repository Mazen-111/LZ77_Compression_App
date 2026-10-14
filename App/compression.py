class TAG:
    def __init__(self, position, length, offset):
        self.position = position
        self.length = length
        self.offset = offset

    def __str__(self):
        return f"<{self.position},{self.length},{self.offset}>"
    

def handle_repetition(text, i, sws, slh):
    best_position = 0
    best_length = 0

    window_start = max(0, i - sws)

    for position in range(1, i - window_start + 1):

        length = 0

        while (length < slh and i + length < len(text) and text[i + length] == text[i - position + (length % position)]):
            length += 1

        if length > best_length:
            best_length = length
            best_position = position

    next_index = i + best_length

    if next_index < len(text):
        offset = text[next_index]
        next_i = next_index + 1
    else:
        offset = None
        next_i = next_index

    return TAG(best_position, best_length, offset), next_i


def lz77_compression(text, sws, slh):
    n = len(text)
    i = 0
    listOfTags = []
    while i < n:
        startOfsw = (i - sws) if (i - sws) >= 0 else 0
        if i == 0:
            sw = ""
        else:
            sw = text[startOfsw:i:1]

        if not text[i] in sw:
            tag = TAG(0,0,text[i])
            listOfTags.append(tag)
            i = i + 1
        else:
            tag, i = handle_repetition(text, i, sws, slh)
            listOfTags.append(tag)

    result = " ".join(str(tag) for tag in listOfTags)
    return listOfTags, result


def save_binary_tags(tags, position_bits, length_bits):
    bits = ""

    for tag in tags:
        bits += format(tag.position, f"0{position_bits}b")

        bits += format(tag.length, f"0{length_bits}b")

        if tag.offset is None:
            bits += "00000000"
        else:
            bits += format(ord(tag.offset), "08b")

    padding = (8-(len(bits) % 8)) % 8
    bits += "0" * padding

    pos_overhead = format(position_bits, "06b")
    len_overhead = format(length_bits, "06b")
    padding_overhead = format(padding, "04b")

    overhead = pos_overhead + len_overhead + padding_overhead

    with open("output.bin", "wb") as file:

        file.write(bytes([int(overhead[i:i + 8], 2) for i in range(0, len(overhead), 8)]))
        
        for i in range(0, len(bits), 8):
            byte = int(bits[i:i + 8], 2)
            file.write(bytes([byte]))

def size_after_compression(tags):
    max_position_bits = max(tag.position for tag in tags).bit_length()
    max_length_bits = max(tag.length for tag in tags).bit_length()
    tag_size = max_position_bits + max_length_bits + 8
    return tag_size, max_position_bits, max_length_bits


def printTags(tagsAsTxt, text, tag_size, tags):
    print("-------------------------------------")
    print("Tags:", end=" ")
    print(tagsAsTxt)
    print('\n')
    print(f"Total Size before Compression: {len(text) * 8} Bits", end="      ")
    print(f"Total Size after Compression: {len(tags) * tag_size} Bits")
    print("-------------------------------------")






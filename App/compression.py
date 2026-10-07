# Tag => <position, length, next symbol>  
class TAG:
    def __init__(self, position, length, offset):
        self.position = position
        self.length = length
        self.offset = offset

# function to handle the repetition
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

    if best_length == 0:
        return TAG(0, 0, text[i]), i + 1

    next_index = i + best_length

    if next_index < len(text):
        offset = text[next_index]
        next_i = next_index + 1
    else:
        offset = None
        next_i = next_index

    return TAG(best_position, best_length, offset), next_i


# compression function
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
    return listOfTags

def size_after_compression(tags):
    max_position_bits = max(tag.position for tag in tags).bit_length()
    max_length_bits = max(tag.length for tag in tags).bit_length()
    tag_size = max_position_bits + max_length_bits + 8
    return tag_size

def printTags(tags, text, tag_size):
    print("-------------------------------------")
    print("Tags:", end=" ")
    for i in tags:
        print(f"<{i.position},{i.length},{i.offset}>", end=" ")
    print('\n')
    print(f"Total Size before Compression: {len(text) * 8} Bits", end="      ")
    print(f"Total Size after Compression: {len(tags) * tag_size} Bits")
    print("-------------------------------------")






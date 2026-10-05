# Tag => <position, length, next symbol>  
class TAG:
    def __init__(self, position, length, offset):
        self.position = position
        self.length = length
        self.offset = offset

# -----------------------------------
# function to handle the repetition =>

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
pass
# -----------------------------------

# compression function
def lz77_compression(text, sws, slh):
    n = len(text) #text length
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
pass

def results():
    # take input from user
    text = input("Enter the text to be compressed: ")
    sws = int(input("Enter the Size of the Search Window: ")) # Size of search window 
    slh = int(input("Enter the size of the Lock a head window: ")) # size of Lock ahead window

    list = lz77_compression(text, sws, slh) # output Tags 

    max_position = max(tag.position for tag in list)
    max_position_bits = max_position.bit_length()

    max_length = max(tag.length for tag in list)
    max_length_bits = max_length.bit_length()

    tag_size = max_position_bits + max_length_bits + 8

    # print the Tags
    print("---------------------------------------------------------------------")
    print("Tags:", end=" ")
    for i in list:
        print(f"<{i.position},{i.length},{i.offset}>", end=" ")
    print("\n---------------------------------------------------------------------")
    print(f"Max Position: {max_position}    Stored in: {max_position_bits} Bits")
    print(f"Max Length: {max_length}      Stored in: {max_length_bits} Bits")
    print(f"Next Symbol is stored in: 8 Bits")
    print("---------------------------------------------------------------------")
    print(f"Tag Size: {max_position_bits} + {max_length_bits} + 8 = {tag_size} Bits")
    print(f"Total Size before Compression: {len(text) * 8} Bits", end="     ")
    print(f"Total Size after Compression: {len(list) * tag_size} Bits")
    print("---------------------------------------------------------------------")






# Tag => <position, length, next symbole>  
class TAG:
    def __init__(self, position, length, offset):
        self.position = position
        self.length = length
        self.offset = offset

# -----------------------------------
# functions to handle the repetition =>

def one_symb_repetition(text, i, slh):
    j = i + 1
    while j <= min(i + slh - 1, len(text) - 1):
        if (len(set(text[i:j + 1])) == 1):
            j += 1
            continue
        else:
            break
    length = len(text[i:j])
    position = 1
    if j < len(text):
        offset = text[j]
    else:
        offset = "NULL"
    return TAG(position, length, offset), j + 1

def two_symb_repetition(text, i, slh):
    j = i + 2
    while j <= min(i + slh - 1, len(text) - 1):
        if (len(set(text[i:j + 1])) == 2):
            j += 1
            continue
        else:
            break
    length = len(text[i:j])
    position = 2
    if j < len(text):
        offset = text[j]
    else:
        offset = "NULL"
    return TAG(position, length, offset), j + 1
# -----------------------------------

# compression function
def lz77_compression(text, sws, slh):
    n = len(text) #text length
    i = 0
    listOfTags = []
    while i < n:
        startOfsw = (i - sws) if (i - sws) >= 0 else 0
        endOfLhw = min(i + slh - 1, n - 1)
        if i == 0:
            sw = ""
        else:
            sw = text[startOfsw:i:1]

        if not text[i] in sw:
            tag = TAG(0,0,text[i])
            listOfTags.append(tag)
            i = i + 1
        else:
            if (text[i] == text[i-1]):
                tag, new_i = one_symb_repetition(text, i, slh)
                listOfTags.append(tag)
                i = new_i
                continue
            if (i > 1 and text[i] == text[i-2] and text[i+1] == text[i-1]):
                tag, new_i = two_symb_repetition(text, i, slh)
                listOfTags.append(tag)
                i = new_i
                continue
            j = i
            while j <= endOfLhw: 
                pattern = text[i:j+1]
                if pattern in sw:
                    j = j + 1   
                    continue
                else:
                    length = len(pattern)-1
                    position = len(sw) - sw.rfind(pattern[:-1])
                    if j < n:
                        offset = text[j]
                    else:
                        offset = "NULL"
                    tag = TAG(position, length, offset)
                    listOfTags.append(tag)
                    i += length + 1
                    break
            if j > endOfLhw:
                pattern = text[i:endOfLhw+1]
                length = len(pattern)
                position = len(sw) - sw.rfind(pattern)

                listOfTags.append(TAG(position, length, "NULL"))
                i += length
        
    return listOfTags


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





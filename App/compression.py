# Tag => <position, length, next symbole>  
class TAG:
    def __init__(self, position, length, offset):
        self.position = position
        self.length = length
        self.offset = offset

# -----------------------------------
# function to handle the repetition =>

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

# print the Tags and Size
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





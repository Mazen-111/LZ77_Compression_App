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
    n = len(text)
    i = 0
    listOfTags = []
    while i < n:
        startOfsw = (i - sws) if (i - sws) >= 0 else 0
        endOfLhw = min(i + slh - 1, n - 1)
        if i == 0:
            sw = ""
        else:
            sw = sw = text[startOfsw:i:1]    

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
                        offset = ""
                    tag = TAG(position, length, offset)
                    listOfTags.append(tag)
                    i += length + 1
                    break
            if j > endOfLhw:
                pattern = text[i:endOfLhw+1]
                length = len(pattern)
                position = len(sw) - sw.rfind(pattern)

                listOfTags.append(TAG(position, length, ""))
                i += length
        
    return listOfTags

                     


    
# take input from user
text = input("Enter the text to be compressed: ")
sws = int(input("Enter the Size of the Window Search: ")) # Size of search window 
slh = int(input("Enter the size of the Lock a head window")) # size of Lock ahead window

n = len(text) # text_length

list = lz77_compression(text, sws, slh) # output Tags 

# print the Tags
for i in list:
    print(f"<{i.position},{i.length},{i.offset}>")





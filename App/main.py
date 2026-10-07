import compression
import decompression

print("================================================================")
print("|               Welcome to LZ77 Compression App                |")
print("================================================================")

print("Choose an option:")
print("1. Compress Text")
print("2. Decompress Text")

while True:
    choice = input("Enter your choice (1 or 2): ")
    if choice == '1':
        #take input from user
        text = input("Enter the text to be compressed: ")
        sws = int(input("Enter the Size of the Search Window: ")) # Size of search window 
        slh = int(input("Enter the size of the Lock a head window: ")) # size of Lock ahead window

        #compressed text
        tags = compression.lz77_compression(text, sws, slh)
        tag_size = compression.size_after_compression(tags)

        #print tags
        compression.printTags(tags, text, tag_size)

        #Do you want to decompress the same text
        answer = input("Do you want to decompress the same compressed text? (y/n): ")
        if answer.lower() == 'y':
            result = decompression.lz77_decompression(tags)
            print("------------------------")
            print("Original Text: " + result)
            print("------------------------")
        print("Thank you for using the LZ77 Compression App!")
        break

    elif choice == '2':
        #take the tages to decompress
        text = input("Enter tags: ")

        #decompress
        result = decompression.lz77_decompression(text)

        #print the original text
        print("---------------------------")
        print("Original Text: " + result)
        print("---------------------------")

        print("Thank you for using the LZ77 Compression App!")
        break


    else:
        print("Invalid choice. Please enter 1 or 2.")

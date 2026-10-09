import compression
import decompression
from tkinter import Tk, filedialog

def takeInput():
    print("\n")
    print("Choose an option:")
    print("1. Enter a Text")
    print("2. choose a file")

    text = ""

    while True:
        choice = input("Enter your choice (1 or 2): ")
        if choice == '1':
            text = input("Enter the text: ") 
            break
        elif choice == '2':
            while True:
                root = Tk()
                root.withdraw()

                file_path = filedialog.askopenfilename(
                    title = "Select Input File",
                    filetypes = [("Text Files", "*.txt")] 
                )

                root.destroy()

                if file_path:
                    with open(file_path, "r", encoding="utf-8") as file:
                        text = file.read()
                    break
            break
        else:
            print("Wrong choice just Enter (1 or 2): ")
    return text

def output(content):
    decision = input("Do you need to sotre the output in a file (y/n): ")
    if decision.lower() == 'y':
        fileName = input("Enter the file name: ")
        with open(fileName, "w", encoding="utf-8") as file:
            file.write(content)


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
        text = takeInput()
        sws = int(input("Enter the Size of the Search Window: ")) # Size of search window 
        slh = int(input("Enter the size of the Lock a head window: ")) # size of Lock ahead window

        #compressed text
        listOfTags,tagsAsTxt = compression.lz77_compression(text, sws, slh)
        tag_size = compression.size_after_compression(listOfTags)

        #print tags
        compression.printTags(tagsAsTxt, text, tag_size, listOfTags)

        # Output File
        output(tagsAsTxt)

        #Do you want to decompress the same text
        answer = input("Do you want to decompress the same compressed text? (y/n): ")
        if answer.lower() == 'y':
            result = decompression.lz77_decompression(listOfTags)
            print("------------------------")
            print("Original Text: " + result)
            print("------------------------")

            # Output File
            output(result)

        print("Thank you for using the LZ77 Compression App!")
        break

    elif choice == '2':
        #take the tages to decompress
        text = takeInput()

        #decompress
        result = decompression.lz77_decompression(text)

        #print the original text
        print("---------------------------")
        print("Original Text: " + result)
        print("---------------------------")

        # Output file
        output(result)

        print("Thank you for using the LZ77 Compression App!")
        break

    else:
        print("Invalid choice. Please enter 1 or 2.")

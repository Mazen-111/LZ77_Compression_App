import compression
import decompression
from tkinter import Tk, filedialog

def takeInput(flag):
    print("\n")
    print("Choose an option:")
    print("1. Enter a Text")
    print("2. choose a Text file")
    if flag == '2':
        print("3. choose a Binary file")

    text = ""

    while True:
        if flag == '1':
            choice = input("Enter your choice (1 or 2): ")
        else:
            choice = input("Enter your choice (1, 2 or 3): ")

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
        elif choice == '3' and flag == '2':
            while True:
                root = Tk()
                root.withdraw()

                file_path = filedialog.askopenfilename(
                    title = "Select Input File",
                    filetypes = [("Binary Files", "*.bin")]
                )

                root.destroy()

                if file_path:
                    with open(file_path, "rb") as file:
                        text = decompression.load_binary_tags(file_path)
                    break
            break
        else:
            print("Wrong choice just Enter (1 or 2): ")
    return text

def output(content):
    decision = input("Do you need to sotre the output in a text file (y/n): ")
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
        text = takeInput(choice)
        sws = int(input("Enter the Size of the Search Window: ")) # Size of search window 
        slh = int(input("Enter the size of the Lock a head window: ")) # size of Lock ahead window

        listOfTags,tagsAsTxt = compression.lz77_compression(text, sws, slh)
        tag_size, max_pos, max_len  = compression.size_after_compression(listOfTags)

        compression.printTags(tagsAsTxt, text, tag_size, listOfTags)

        compression.save_binary_tags(listOfTags, max_pos, max_len)

        answer = input("Do you want to decompress the same compressed text? (y/n): ")
        if answer.lower() == 'y':
            result = decompression.lz77_decompression(listOfTags)
            print("------------------------")
            print("Original Text: " + result)
            print("------------------------")

            output(result)
        print("Thank you for using the LZ77 Compression App!")
        break

    elif choice == '2':
        text = takeInput(choice)

        result = decompression.lz77_decompression(text)

        print("---------------------------")
        print("Original Text: " + result)
        print("---------------------------")

        output(result)

        print("Thank you for using the LZ77 Compression App!")
        break

    else:
        print("Invalid choice. Please enter 1 or 2.")

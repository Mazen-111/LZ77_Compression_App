import compression
import decompression

print("================================================================")
print("=============== Welcome to LZ77 Compression App ================")
print("================================================================")

print("Choose an option:")
print("1. Compress Text")
print("2. Decompress Text")
while True:
    choice = input("Enter your choice (1 or 2): ")
    if choice == '1':
        compression.results()
        answer = input("Do you want to decompress a text? (y/n): ")
        if answer.lower() == 'y':
            decompression.decompress_text()
        print("Thank you for using the LZ77 Compression App!")
        break
    elif choice == '2':
        decompression.decompress_text()
        answer = input("Do you want to compress a text? (y/n): ")
        if answer.lower() == 'y':
            compression.results()
        else:
            print("Thank you for using the LZ77 Compression App!")
            break
    else:
        print("Invalid choice. Please enter 1 or 2.")

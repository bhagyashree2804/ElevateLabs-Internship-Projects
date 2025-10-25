# main.py
from crypto_utils import encrypt_file, decrypt_file

def main():
    print("=== Secure File Storage System ===")
    print("1. Encrypt a file")
    print("2. Decrypt a file")
    choice = input("Choose an option (1/2): ")

    if choice == '1':
        path = input("Enter the path of the file to encrypt: ")
        pwd = input("Enter a password: ")
        encrypt_file(path, pwd)
    elif choice == '2':
        path = input("Enter the path of the encrypted file (.enc): ")
        pwd = input("Enter the password: ")
        decrypt_file(path, pwd)
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()

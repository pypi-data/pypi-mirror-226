import os
import sys
import random
import string
from cryptography.fernet import Fernet


def generate_random_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def encrypt_file(file_path, password):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    with open(file_path, 'rb') as file:
        file_data = file.read()

    encrypted_data = cipher_suite.encrypt(file_data)

    encrypted_file_path = file_path + '.encrypted'
    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

    return key

def decrypt_file(encrypted_file_path, key):
    cipher_suite = Fernet(key)

    with open(encrypted_file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()

    decrypted_data = cipher_suite.decrypt(encrypted_data)

    decrypted_file_path = encrypted_file_path.replace('.encrypted', '.decrypted')
    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

if __name__ == "__main__":
    file_path = input("Digite o caminho do arquivo que você deseja criptografar: ")

    if not os.path.exists(file_path):
        print("Arquivo não encontrado.")
        sys.exit(1)

    password = generate_random_password()
    key = encrypt_file(file_path, password)
    print(f'Arquivo criptografado: {file_path}')
    print(f'Senha: {password}')

    encrypted_file_path = file_path + '.encrypted'
    senha_usuario = input("Digite a senha para descriptografar: ")
    if password == senha_usuario:
        decrypt_file(encrypted_file_path, key)
        print(f'Arquivo descriptografado: {encrypted_file_path.replace(".encrypted", ".decrypted")}')
    else:
        print("Senha incorreta. Não é possível descriptografar o arquivo.")
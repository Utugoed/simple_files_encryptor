import argparse
from cryptography.fernet import Fernet
import os



class Encryptor:

    def __init__(self):
        key_exists = os.path.exists('encryptor_key.key')
        if key_exists:
            with open('encryptor_key.key', 'rb') as key:
                self.key = key.read()
        else:
            self.key = Fernet.generate_key()
            with open('encryptor_key.key', 'wb') as key:
                key.write(self.key)
        
        self.files = []
        self.ignore = ['./encryptor.py', './encryptor_key.key']
        self.__collect_files(cur_dir='.')
    
    def __collect_files(self, cur_dir):
        for file in os.listdir(cur_dir):
            full_file = f'{cur_dir}/{file}'
            if full_file in self.ignore:
                continue
            if os.path.isfile(full_file):
                self.files.append(full_file)
                continue
            self.__collect_files(cur_dir=full_file)
    
    def encrypt(self):
        for file in self.files:
            with open(file, 'rb') as rfile:
                content = rfile.read()
            encrypted_content = Fernet(self.key).encrypt(content)
            with open(file, 'wb') as wfile:
                wfile.write(encrypted_content)
    
    def decrypt(self):
        for file in self.files:
            with open(file, 'rb') as rfile:
                content = rfile.read()
            decrypted_content = Fernet(self.key).decrypt(content)
            with open(file, 'wb') as wfile:
                wfile.write(decrypted_content)


if __name__ == '__main__':
    encryptor = Encryptor()

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-d', '--decrypt', action='store_true', required=0)
    arg_parser.add_argument('-l', '--files_list', action='store_true', required=0)
    arg_parser.add_argument('-e', '--encrypt', action='store_true', required=0)

    args = arg_parser.parse_args()

    if args.decrypt:
        encryptor.decrypt()
    elif args.files_list:
        print(encryptor.files)
    elif args.encrypt:
        encryptor.encrypt()
    else:
        arg_parser.print_help()
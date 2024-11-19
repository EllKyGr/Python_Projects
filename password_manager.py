# import json
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
from os.path import exists
import base64
import time
# Organize and store your passwords as an encrypted format


def save_Mpw(password: str) -> list[bytes]:
    """
    Creates and returns encrypted mpw with key

    :param password: A string format password designed by user
    :return: master password with its decryption key
    :rtype: list[bytes]

    :Example:
    >>> save_Mpw("plop")
    [b"gAAAAABnLUo...", b"Xu4jTgklzZm..."]
    """
    key: bytes = Fernet.generate_key()
    fer: Fernet = Fernet(key)  # Handle use for encryption and decryption
    token: bytes = fer.encrypt(password.encode())
    return [token, key]


# os.urandom() uses system entropy sources for better random generation
def create_key_from_password(password: bytes, file: str, mpw_k: bytes,
                             salt: bytes = os.urandom(16)) -> None:
    """
    Creates main key and stores it mpw and its key

    :param password: First returned value from `save_Mpw()` function
    :type password: bytes
    :param file: Name of `.key` file
    :type file: str
    :param mpw_k: Second returned value from `save_Mpw()` function
    :type mpw_k: bytes
    :param salt: Default set to 16 characters
    :type salt: bytes
    :return: None
    :rtype: NoneType
    """
    # Creates the main key to store and visualize file content
    # Key Derivation Function
    kdf = PBKDF2HMAC(  # Derives a key from a password, using a salt and iter
        algorithm=hashes.SHA256(),  # cryptographic hash function 256 bits
        length=32,
        salt=salt,  # aleatory string of characters
        iterations=600000  # The higher the number, slower the algorithm, safer
    )
    # base64 converts bytes that have binary or text data into ASCII characters
    key = base64.urlsafe_b64encode(kdf.derive(password))

    with open(file, "wb") as key_file:
        key_file.write(key + "\n".encode())
        key_file.write(password + "\n".encode())
        key_file.write(mpw_k + "\n".encode())


def load_key(file: str) -> Fernet:
    """
    Loads main key to visualize data

    :param file: Name of `.key` file
    :type file: str
    :return: Fernet handle to decrypt keys file
    :rtype: Fernet
    """
    with open(file, "rb") as file_key:
        data = file_key.read()
        content = data.decode().split("\n")
    key: bytes = content[0].encode()
    return Fernet(key)


def validate_mpw(fer: Fernet, file: str) -> bytes:
    """
    Decrypts the stored mpw from file

    :param fer: returned value from `read_mpw()` function
    :type fer: Fernet
    :param file: Name of `.key` file
    :type file: str
    :return: Decrypted master password
    :rtype: bytes
    """
    with open(file, "rb") as fl:
        data = fl.read()
        content = data.split("\n".encode())
    mpw = content[1]
    # print(fer.decrypt(mpw))
    return fer.decrypt(mpw)


def MPw_validation_saving(mpw: str, fer: Fernet, file: str) -> bool:
    """
    Compares recent entered MPass with the saved one in file

    :param mpw: Most recent master password entered
    :type mpw: str
    :param fer: returned value from `read_mpw()` function
    :type fer: Fernet
    :param file: Name of `.key` file
    :return: True or False
    :rtype: bool
    """
    return validate_mpw(fer, file) == mpw.encode()


def add(fer: Fernet) -> None:
    """
    Store and encrypt users input

    :param fer: Encrypts user input
    :type fer:
    :return: None
    :rtype: NoneType
    """
    usr: str = input("Account: ")
    pwd: str = input("Password: ")
    with open("keys.txt", "a") as file:
        # Writes to the file in a string like format the encrypted version
        # of the password previously encoded in utf-8
        file.write(usr + "|" + fer.encrypt(pwd.encode()).decode() + "\n")


def view(fer: Fernet) -> None:  # Add secondary selection to return just one
    """
    Read unencrypted data

    :param fer: Decrypts user input
    :type fer:
    :return: None
    :rtype: NoneType
    """
    if not exists("./keys.txt"):
        print("Unable to find 'keys.txt', creating it", end='')
        with open("keys.txt", "w") as file:
            for n in range(3):
                print(".", end='', flush=True)
                time.sleep(1)
        print()
    else:
        if os.path.getsize("./keys.txt") < 1:
            print("No entries currently found in file. Add some first.")
        else:
            with open("keys.txt", "r") as file:
                for line in file.readlines():
                    data: str = line.rstrip()
                    usr, pwd = data.split("|")
                    print(usr, fer.decrypt(pwd.encode()).decode())


def read_mpw(file: str) -> Fernet:
    """
    Retrieve key for decrypting mpw

    :param file: Name of `.key` file
    :type file: str
    :return: Fernet wrapper for mpw decryption
    :rtype: Fernet
    """
    with open(file, "rb") as fl:
        content = fl.read()
        data = content.split("\n".encode())
    fer = Fernet(data[2])
    return fer


def add_view(fer: Fernet) -> None:
    """
    Create and read account/site and password

    :param fer: Fernet wrapper from main key
    :type fer: Fernet
    :return: None
    :rtype: NoneType
    """
    # Invalid entry will terminate the program
    while True:
        # Ask the user whether add or read the password(s)
        mode: str = input("V or A: ").lower()
        if mode == "q":
            break
        if mode == "v":
            view(fer)
        elif mode == "a":
            add(fer)
        else:
            print("Invalid")
            sys.exit()


# Might split this in two instead
def main() -> None:
    file: str = "key.key"  # Might use regex if key's name changes
    m_pwd: str = input("Enter MPass: ")
    if not exists(file):
        # Create the master password first, then pass it to the main key
        mpw, mpw_key = save_Mpw(m_pwd)
        print("Key file missing in current directory.\n"
              f"Creating key as '{file}'", end='')
        # Stores main key, mpw and mpw key
        create_key_from_password(mpw, file, mpw_key)
        for n in range(3):
            print(".", end='', flush=True)
            time.sleep(1)
        print()
    if exists(file):
        print("Verifying users entry", end='')
        for n in range(3):
            print('.', end='', flush=True)
            time.sleep(1)
        print()
        # Read stored mpw key
        fer = read_mpw(file)
        # Reads and validates mpw to get access to main key
        if MPw_validation_saving(m_pwd, fer, file):
            # Handle for initializing
            key: Fernet = load_key(file)
            add_view(key)
        else:
            # Wrong password will terminate the program
            print("Invalid MPass")
            sys.exit()


if __name__ == "__main__":
    # pass
    main()
    # create_key_from_password("plop")

# := assigns to a variable inside an expression if (x:=5) == True

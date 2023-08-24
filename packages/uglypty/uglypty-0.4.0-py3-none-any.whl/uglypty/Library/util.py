import os

from cryptography.fernet import Fernet


def cryptonomicon(to_decrypt, key_path="./crypto.key"):
    from cryptography.fernet import Fernet

    try:
        # load crypto key - and sanity check
        fhc = open(key_path, "r")
        key = fhc.read()
        key = key.strip()
        cryptonizer = Fernet(key)

        to_decrypt = bytes(to_decrypt, 'utf-8')
        result = cryptonizer.decrypt(to_decrypt)

        return result.decode("utf-8")
    except Exception as e:
        print("error processing crypto key file")
        raise e

def encrypt(to_encrypt):
    from cryptography.fernet import Fernet
    try:
        # load crypto key - and sanity check
        fhc = open("crypto.key", "r")
        key = fhc.read()
        key = key.strip()
        cryptonizer = Fernet(key)
        to_encrypt = bytes(str(to_encrypt), 'utf-8')
        result = cryptonizer.encrypt(to_encrypt)
        return result
    except Exception as e:
        print("error processing crypto key file")

def generate_key():

    # Check if the file exists
    if os.path.isfile('crypto.key'):
        # Ask the user for confirmation
        confirm = input(
            'The file "crypto.key" already exists, do you want to overwrite it? This will invalidate your currently encrypted passwords. (y/n): ')

        # Check the user's response
        if confirm.lower() != 'y':
            print('Operation cancelled.')
            exit()

    # Generate a key
    key = Fernet.generate_key()

    # Save the key to the file
    with open('crypto.key', 'wb') as file:
        file.write(key)

    print('Key saved to "crypto.key".')

def create_db():
    import sqlite3

    conn = sqlite3.connect('settings.sqlite')
    c = conn.cursor()

    c.execute('''
              CREATE TABLE "creds" (
    	"id" INTEGER NOT NULL  ,
    	"username" TEXT NULL  ,
    	"password" TEXT NULL
    , "displayname"	TEXT)
              ''')

    conn.commit()
    print("settings.sqlite created")
# This is a simple encryption library
# Developed by ADJEI COLLINS.
#
# ADJEI COLLINS is a Cybersecurity student from Accra Technical University, Ghana.
#
# FUNCTIONS
# __________
# encryption,
# decryption,
# saving,
# reading files(encrypted messages) for decryption,
# and displaying messages.

#Usage guide is beneath the code

import base64

class EncryptMe:
    def __init__(self, message):
        self.message = message

    def save(self, filename):
        with open(filename, 'w') as file:
            file.write(self.message)
            print("Message encrypted and saved:", filename)

    def show(self):
        print(self.message)

def encrypt(message, key):
    encrypted_bytes = bytearray((c + key) % 256 for c in message.encode('utf-8'))
    encrypted_text = base64.b64encode(encrypted_bytes).decode('utf-8')
    return EncryptMe(encrypted_text)

def decrypt(encrypted_text, key):
    try:
        encrypted_bytes = base64.b64decode(encrypted_text.encode('utf-8'))
        decrypted_bytes = bytearray((c - key) % 256 for c in encrypted_bytes)
        decrypted_text = decrypted_bytes.decode('utf-8')
        return EncryptMe(decrypted_text)
    except:
        return EncryptMe("Invalid key or input for decryption")

def save(data, filename):
    try:
        with open(filename, 'w') as file:
            file.write(data)
            print("Data saved to:", filename)
    except Exception as e:
        print("Error:", e)

def read(filename):
    try:
        with open(filename, 'r') as file:
            data = file.read()
        return data
    except FileNotFoundError:
        print("File not found or invalid directory")
        return None
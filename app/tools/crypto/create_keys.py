# -*- coding: utf-8 -*-
# Module 'create_keys' of the project 'tingerwork'
# :date_create: 10.12.2017.18:24
# :author: Tingerlink
# :description:


from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
import base64


def generate_RSA(bits=1024):
    new_key = RSA.generate(bits, e=65537)
    public_key = new_key.publickey().exportKey("PEM")
    private_key = new_key.exportKey("PEM")

    with open('private_rsa_key.bin', 'wb') as f:
        f.write(private_key)

    with open('public_rsa_key.bin', 'wb') as f:
        f.write(public_key)

    return private_key, private_key


def doRSAFromBytes(key, plaintext):
    # Assuming that the public key is coming from java or javascript,
    # strip off the headers.
    key = key.replace('-----BEGIN PUBLIC KEY-----', '')
    key = key.replace('-----END PUBLIC KEY-----', '')
    # Since it's coming from java/javascript, it's base 64 encoded.
    # Decode before importing.
    pubkey = RSA.importKey(base64.b64decode(key))
    cipher = PKCS1_OAEP.new(pubkey, hashAlgo=SHA256)
    encrypted = cipher.encrypt(plaintext)
    print(base64.b64encode(encrypted))
    return base64.b64encode(encrypted)


def decryptRSA(ciphertext, private_key):
    rsa_key = RSA.importKey(private_key)
    cipher = PKCS1_OAEP.new(rsa_key, hashAlgo=SHA256)
    decrypted = cipher.decrypt(base64.b64decode(ciphertext))
    return decrypted

generate_RSA()

ct = doRSAFromBytes(open('my_rsa_public.pem', 'r').read(), "hello".encode('utf-8'))

print(decryptRSA(ct, open('my_private_rsa_key.bin', 'r').read()))
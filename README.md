About this Repository
==================================

This repository contains two programs. One of the programs scans a single-paged document and encrypts the bytes of that document. The other program decrypts the encrypted bytes.

In order to run these programs, you will need to have the following installed on your computer:

1. SANE - http://www.sane-project.org/source.html 
2. Pillow - https://github.com/python-pillow/Pillow
3. Pycrypto - https://www.dlitz.net/software/pycrypto/

SANE is used to perform the actual scan, Pillow works with SANE to display scanned images, and Pycrypto is used for encryption.


About the Files
==================================
encryptionScanner.py is the script that performs a single-page scan and encrypts the bytes from that scan. Encryption is performed using AES (American Encryption Standard) with a cipher block mode of operation. 

fileDecryption.py is the script that decrypts the encrypted documents.

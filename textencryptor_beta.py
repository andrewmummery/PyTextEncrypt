"""
TextEncryptor

A number of simple algorithms which will encrypt plain text. 

Author: 
Andrew Mummery, 
Oxford University Astrophysics,
andrew.mummery.software@gmail.com 

git repo: https://github.com/andrewmummery/TextEncryptor

Functions for user:

This package contains a number of functions which are used for 
encrypting and decrypting text files and plain text. The important
functions for the user are the following

1. textencryptor.encrypt_file() 
2. textencryptor.decrypt_file()
3. textencryptor.encrypt_message()
4. textencryptor.decrypt_message()
5. textencryptor.send_encrypted_email()

Functions 1 & 3 work by encrypting either a user specified 
text file (1.), or a user given message (3.), using a user
given encryption pin/password. 

The encrypted text file or message can be later decrypted
using functions (2.) or (4.), provided that the decryption
pin is identical to the pin used for encryption.  

Function (5.) uses encrypt_message() to encrypt some plain text.
This plain text is then sent in an email. Note that this currently
only works with gmail. Some modifications to your gmail account 
settings will be required. By default gmail will block pythons 
attempts to log in to your gmail account, as it deems it insecure.
    
To allow python access to your gmail, go to the following link
https://myaccount.google.com/lesssecureapps
and switch 'allow less secure apps' to ON. 

**Notes:**

I. No inputs are required for the five main functions, if 
left as, e.g. textencryptor.encrypt_file(), the user will be 
prompted for the required infromation, in this example:

a. The path to the file to be encrypted.
b. The encryption pin. 
c. The path for the encrypted file to be saved to. 

This information can of course be input, then no information
will be required from the user, e.g. 

textencryptor.encrypt_file(load_file_path='example.txt', pin = 123456, save_file_path='encrypted_example.txt')

will create an encrypted file named encrypted_example.txt.
This file is an ecnrypted version of the file example.txt
with encryption pin = 123456. 

II. The algorithms in this package are hard coded in the 
english language. Symbols used in many european languages
(e.g. Å,Ê,Î,Ó,Ù etc...) will be lost in the encryption
and decryption proccess.  

III. send_encrypted_email() ONLY works with gmail. See the 
send_emcrypted_email() function for more information. 

IV. Some more information on the mathematics underpining the 
encryption/decryption algorithms is contained at the bottom
of this file. 

"""

import sys

def printProgressBar(Q,tot,preText):
    """
    A simple funciton for displaying the progress through various stages 
    of the encryption/decryption algorithms.
    """
    n_bar =30 #size of progress bar
    q = Q/tot
    sys.stdout.write('\r')
    sys.stdout.write(f" {preText} [{'=' * int(n_bar * q):{n_bar}s}] ")
    sys.stdout.flush()

def key_from_pin(pin,length_message):
    """
    This function creates a binary key-stream of length "length_message" from an input
    pin "pin". 
    
    This pin is first represented by a binary string of length n0.
    
    The key stream is generated by XORing the jth and (j+n0-1)th binary digits of the 
    key stream together to get the (j+n0)th binary digit of the key. This continues until
    the key stream is the same length as "length_message". 
    
    A key stream generated in this manner repeats after 2^n0 - 1 binary digits. 
    
    The idea behind this method is taken from page 65 of AVSI: Cryptography, Piper & Murphy
    """
    k = bin(pin)[2:]
    j=0
    n0 = len(k)
    while j < length_message-n0:
        s1 = int(k[j])
        s2 = int(k[j+n0-1])
        p = s1 ^ s2# XOR operation. 
        k=k+str(p)
        j+=1
        if (100*(j+1)) % round(length_message-n0+5,-1) == 0:
            printProgressBar(j+1,length_message-n0,"Key generation:")
    printProgressBar(j+1,length_message-n0,"Key generation:")    
    print()
    return k

def key_from_password(password,length_message):
    """
    This function creates a binary key-stream of length "length_message" from an input
    alpha-numerical password "password". 
    
    This password is first transformed into a binary string of length n0. This transformation
    uses the 'library()' function which maps alpha-numeric strings to binary representations. 
    
    The key stream is then generated by XORing the jth and (j+n0-1)th binary digits of the 
    key stream together to get the (j+n0)th binary digit of the key. This continues until
    the key stream is the same length as "length_message". 
    
    A key stream generated in this manner repeats after 2^n0 - 1 binary digits. 
    
    The idea behind this method is taken from page 65 of AVSI: Cryptography, Piper & Murphy
    """
    k = message_to_binary(password)
    j=0
    n0 = len(k)
    while j < length_message-n0:
        s1 = int(k[j])
        s2 = int(k[j+n0-1])
        p = s1 ^ s2
        k=k+str(p)
        j+=1
        if (100*(j+1)) % round(length_message-n0+5,-1) == 0:
            printProgressBar(j+1,length_message-n0,"Key generation:")
    printProgressBar(j+1,length_message-n0,"Key generation:")    
    print()
    return k
    
def library():
    """
    Returns the 'library' and 'numbrary' used for mapping between alpha-numeric characters 
    and binary representations of length 7. There are a total of 128 alpha-numeric characters 
    which can be used in the (encrypted/plaintext) messages. Each character in the library 
    has a corresponding integer in the 'numbrary', and so can be represented by a unique 
    binary string of length 7. 
    
    i.e. 
    a -> 0 = 0000000
    ! -> 39 = 0100111
    
    The integer to binary mapping is done in the encryption loops.
    
    IMPORTANT NOTE: If an alpha-numeric character is not in the library then it cannot be
    encrypted and will be lost during the encryption/decryption process. 
    """
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    numberbet = ['0','1','2','3','4','5','6','7','8','9']
    punctuation = ['.',',','!','?',':',';','=','+','-','(',')','"','£','%','$','^','&',' ','/','[',']','*','@','_','<','>',"'"]
    Alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    misc = ['œ','∑','®','†','¥','|','`','π','å','ß','∂','ƒ','©','´','∆','˚','¬','Ω','≈','ç','√','∫','~','µ','≤','≥','÷','≠','€','#','∞','§','•','\n','Ø','Æ','Ÿ','∏','◊']
    lib = alphabet + numberbet + punctuation + Alphabet + misc
    nib = []
    for j in range(len(lib)):
        nib.append(j)
    return lib, nib
    
def message_to_binary(message):
    """
    Takes a message in plaintext and converts into a binary string. 
    Each character in the message, if its is in the library, is converted
    to the corresponding integer in the numbrary. This integer is then
    represented as a 7 digit binary string. 
    """
    lib, nib = library()
    binary_message = str()
    i, n_char = 0, len(message)
    for char in message:
        j = 0
        for let in lib:
            if char == let:
                binary_message += bin(nib[j])[2:].zfill(7)# pads with zeros to ensure 7 digits long.
            j+=1
        i+=1
        if ((i+1)*100) % round(n_char+5,-1) == 0:
            printProgressBar(i+1,n_char,"Alpha-numeric -> binary:")
    printProgressBar(i+1,n_char,"Alpha-numeric -> binary:")
    print()
    return binary_message

def binary_to_message(binary_message):
    """
    Takes a binary string and converts into a alpha-numeric text message.
    In effect the opposite of the function message_to_binary().
    The binary string is split into 7 digit sub-strings. These sub-strings
    are represented by an integer, and then replaced by the character in 
    the library with the equivalent numbrary integer. 
    """
    lib, nib = library()
    text_message = str()
    le = len(binary_message)
    if le % 7 != 0:
        print('WARNING: BINARY MESSAGE WRONG LENGTH.')
    else:
        n_char = int(le/7)
        for j in range(n_char):
            binary_str = binary_message[7*j:7*(j+1)]# The binary string for a particular character
            int_char = int(binary_str, 2)# Character converted into its integer representation
            i = 0
            for num in nib:
                if num == int_char:
                    text_message += lib[i]
                i+=1
            if (100*(j+1)) % round(n_char+5,-1) == 0:
                printProgressBar(j+1,n_char,"Binary -> alpha-numeric:")
    printProgressBar(j+1,n_char,"Binary -> alpha-numeric:")
    print()
    return text_message

def encrypt_binary_stream_cipher(message_in_binary, key_string):
    """
    Takes a single key stream of the same length as the message, 
    then computes an encrypted binary stream by XORing the two 
    together. 
    
    Key stream should be computed by the function key_from_pin, or key_from_password. 
    """
    encrypted_binary = str()
    if len(message_in_binary) != len(key_string):
        print('The key provided is a different length to the message.')
    else:
        le = len(message_in_binary)
        if le % 7 != 0:
            print('WARNING: BINARY MESSAGE WRONG LENGTH.')
        else:
            message_integer = int(message_in_binary, 2)
            key_integer = int(key_string, 2)
            encrypted_integer = message_integer ^ key_integer 
            encrypted_binary = bin(encrypted_integer)[2:].zfill(le)
    return encrypted_binary

def decrypt_binary_stream_cipher(message_in_binary, key_string):
    """
    The stream cipher is perfectly symmetric, and so encryption and
    decryption are the same. Just given a name for ease of reading. 
    """
    decrypted_binary = encrypt_binary_stream_cipher(message_in_binary, key_string)
    return decrypted_binary

def encrypt_binary_cipher_block_chaining(message_in_binary, key_string):
    """
    This is a more sophisticated approach to encrypting a binary string.
    This method is based off of the method described on page 90 of 
    AVSI: Cryptography, Piper & Murphy.
    
    In this cipher the encryption of a character depends both on the key_stream
    but also on its location within the text. For particularly simple keys 
    (i.e a single letter key) this prevents the code from being susceptible to 
    attacks based on the structure of the english language. It does this by
    flattening the character-frequency distribution in the encrypted text. 
    
    Schematically the encryption process is the following.
    
    (Arrows in flow diagram should be followed in intuitive fashion.)
    
    [+] = binary XOR operation. 
    Properties of the XOR operation are discussed at the bottom of this file. 
    
    INPUT:   p_1                     p_2
              |                       |
              v                       v
              |                       |
       iv ->-[+]            ---->----[+]                 --- > ......
              |             |         |                  |
             i_1            |        i_2                 |
              |             |         |                  |
              v             |         v                  |
              |             ^         |                  ^
    KEY:     [+]--<-- k_1   |        [+]--<-- k_2        |
              |             |         |                  |
              v             |         v                  |
              |             |         |                  |
             c_1------>-----|        c_2-------->--------|
              |                       |
              |                       |
    OUTPUT:   •                       •
    
    1. We split the input binary string and key into blocks of length 7
    
    MESSAGE -> p_1, p_2, p_3, ....
    
    KEY -> k_1, k_2, k_2, ....
    
    2. For the very first plaintext string, we XOR it with an
    'initial value' string, here hardcoded as 0101010. This produces
    an intermediate string i_1. 
    
    4. The ciphertext is then found by XORing this intermediate string 
    with the key stream. 
    
    5. For all other pieces of the plaintext we XOR the previous ciphertext
    c_{j-1} with the current plaintext p_{j} to form the intermediate string
    i_{j}, which is then encrypted with key string k_{j} using the XOR operation. 
    
    As is clear to see (below), c_{j} depends both on the key k_{i≤j}, the initial value iv,
    and all previous p_{i<j}
    
    c_{j} = i_{j} [+] k_{j} = (c_{j-1} [+] p_{j}) [+] k_{j} 
          = ((i_{j-1} [+] k_{j-1}) [+] p_{j}) [+] k_{j}
          = (((c_{j-2} [+] p_{j-1}) [+] k_{j-1}) [+] p_{j}) [+] k_{j}
          = .....
    """
    encrypted_binary = str()
    iv = '0101010'
    iv = int(iv,2)
    if len(message_in_binary) != len(key_string):
        print('The key provided is a different length to the message.')
    else:
        le = len(message_in_binary)
        if le % 7 != 0:
            print('WARNING: BINARY MESSAGE WRONG LENGTH.')
        else:
            n_char = int(le/7)
            for j in range(n_char):
                p_j = int(message_in_binary[7*j:7*(j+1)], 2)
                key_j = int(key_string[7*j:7*(j+1)], 2)
                if j == 0:
                    i_j = iv ^ p_j
                else:
                    c_j_1 = int(encrypted_binary[7*(j-1):7*j], 2)
                    i_j = c_j_1 ^ p_j
                encrypted_integer = key_j ^ i_j
                encrypted_binary += bin(encrypted_integer)[2:].zfill(7)
                if (100*(j+1)) % round(n_char+5,-1) == 0:
                    printProgressBar(j+1,n_char,"Encrypting: ")
    printProgressBar(j+1,n_char,"Encrypting: ")
    print()
    return encrypted_binary

def decrypt_binary_cipher_block_chaining(message_in_binary, key_string, line_breaks=True):
    """
    This function inverts the 'cipher block chaining' encryption algorithm.
    The encryption algorithm is described above. 
    
    As this is an inversion of the above program, it has a slightly 
    different structure. This structure is described schematically below:
    
    (Arrows in flow diagram should be followed in intuitive fashion.)
    
    [+] = binary XOR operation.
    Properties of the XOR operation are discussed at the bottom of this file. 
    
    INPUT:   c_1 ----->-----|        c_2 ------->------| 
              |             |         |                |
              v             |         v                |
              |             |         |                |
    KEY:     [+] --<-- k_1  |        [+] --<-- k_2     |             
              |             v         |                v
             i_1            |        i_2               |
              |             |         |                |
              v             |         v                |
              |             |         |                |
      iv ----[+]            ----->---[+]               --->---  ......
              |                       |                  
              |                       |                  
             p_1                     p_2
              |                       |
              |                       |
    OUTPUT:   •                       •
    
    """
    decrypted_binary = str()
    iv = '0101010'# I must be the same as the encryption algorithm or I will fail. 
    iv = int(iv,2)
    if len(message_in_binary) != len(key_string):
        print('The key provided is a different length to the message.')
    else:
        le = len(message_in_binary)
        if le % 7 != 0:
            print('WARNING: BINARY MESSAGE WRONG LENGTH.')
        else:
            n_char = int(le/7)
            for j in range(n_char):
                c_j = int(message_in_binary[7*j:7*(j+1)], 2)
                key_j = int(key_string[7*j:7*(j+1)], 2)
                i_j = c_j ^ key_j
                if j == 0:
                    p_j = iv ^ i_j
                else:
                    c_j_1 = int(message_in_binary[7*(j-1):7*j], 2)
                    p_j = c_j_1 ^ i_j
                decrypted_binary += bin(p_j)[2:].zfill(7)
                if (100*(j+1)) % round(n_char+5,-1) == 0:
                    printProgressBar(j+1,n_char,"Decrypting:")
    printProgressBar(j+1,n_char,"Decrypting:")
    print()
    return decrypted_binary


def file_to_message(file_name='encrypt_me.txt'):
    """
    This function simply reads a text file (with name file_name) to a string. 
    """
    message = str()
    with open(file_name) as fp:
        for line in fp:
            message += line
    return message

def message_to_file(message,save_name='encrypted_file.txt'):
    """
    This function saves a string to a text file (with name save_name). 
    """
    sf = open(save_name,'w+')
    sf.write(message)
    sf.close()

def encrypt_file(load_file_path=None, save_file_path=None, pin=None,algorithm='CBC'):
    """
    This funciton encrypts a text file. It then saves an ecrypted version of the file. 
    
    If simply called as: 
    
    PyTextEncrypt.encrypt_file()
    
    the user will be prompted to input:
     
    load_file_path = path to the text file to be encrypted.
    pin = the encryption pin. Can be a numeric pin or alpha-numeric password.
    save_file_path = the location where the encrypted text file will be saved.
    
    """
    if load_file_path != None:
        message = file_to_message(load_file_path)
        binary_message = message_to_binary(message)
    else:
        print()
        load_file_path = input('Path to file to be encrypted: ')
        print()
        message = file_to_message(load_file_path)
        binary_message = message_to_binary(message)
        
    if pin != None:
        pin = str(pin)
        if pin.isnumeric():
            key = key_from_pin(int(pin),len(binary_message))
        else:
            key = key_from_password(pin,len(binary_message))
    else:
        print()
        pin = input('Encryption Pin: ')
        print()
        if pin.isnumeric():
            key = key_from_pin(int(pin),len(binary_message))
        else:
            key = key_from_password(pin,len(binary_message))
    
    if algorithm == 'CBC':
        encrypted_binary = encrypt_binary_cipher_block_chaining(binary_message, key)
    else:
        encrypted_binary = encrypt_binary_stream_cipher(binary_message, key)
    
    encrypted_message = binary_to_message(encrypted_binary)
    
    if save_file_path != None:
        message_to_file(encrypted_message,save_file_path)
    else:
        print()
        save_file_path = input('Name and path for encrypted file: ')
        print()
        message_to_file(encrypted_message,save_file_path)
    

def decrypt_file(load_file_path=None, save_file_path=None, pin=None,algorithm='CBC'):
    """
    This funciton decrypts an encrypted text file. It then saves the decrypted version of the file. 
    
    If simply called as: 
    
    PyTextEncrypt.decrypt_file()
    
    the user will be prompted to input:
     
    load_file_path = path to the text file to be decrypted.
    pin = the encryption pin. Can be a numeric pin or alpha-numeric password.
    save_file_path = the location where the decrypted text file will be saved.
    
    """
    
    if load_file_path != None:
        encrypted_message = file_to_message(load_file_path)
        encrypted_binary = message_to_binary(encrypted_message)
    else:
        print()
        load_file_path = input('Path to file to be decrypted: ')
        print()
        encrypted_message = file_to_message(load_file_path)
        encrypted_binary = message_to_binary(encrypted_message)
        
    if pin != None:
        pin = str(pin)
        if pin.isnumeric():
            key = key_from_pin(int(pin),len(encrypted_binary))
        else:
            key = key_from_password(pin,len(encrypted_binary))
    else:
        print()
        pin = input('Decryption Pin: ')
        print()
        if pin.isnumeric():
            key = key_from_pin(int(pin),len(encrypted_binary))
        else:
            key = key_from_password(pin,len(encrypted_binary))
    
    if algorithm == 'CBC':
        decrypted_binary = decrypt_binary_cipher_block_chaining(encrypted_binary, key)
    else:
        decrypted_binary = decrypt_binary_stream_cipher(encrypted_binary, key)
    
    message = binary_to_message(decrypted_binary)
    if save_file_path != None:
        message_to_file(message,save_file_path)
    else:
        print()
        save_file_path = input('Name and path for decrypted file: ')
        print()
        message_to_file(message,save_file_path)


def encrypt_message(message=None, pin=None, algorithm='CBC', save_encrypted_message = False, save_file_path = 'encrypted_message.txt'):
    """
    This funciton encrypts a 'message', not taken from a file. 
    It can then either print or save an ecrypted version of this message.
    
    If simply called as: 
    
    PyTextEncrypt.encrypt_message()
    
    the user will be prompted to input:
     
    message = the message to be encrypted
    pin = the encryption pin. Can be a numeric pin or alpha-numeric password.
    
    if save_encrypted_message is set True then the encrypted message will be 
    saved as a text file, at location save_file_path. 
    
    I strongly recommend saving the encrypted message. This is because errors
    can propogate when copying and pasting from the terminal. 
    
    """
    
    if message != None:
        binary_message = message_to_binary(message)
    else:
        print('Message to be encrypted: (When done press enter then control+D [mac] or control+Z [windows]). ')
        message = sys.stdin.read()
        print()
        binary_message = message_to_binary(message)
        
    if pin != None:
        pin = str(pin)
        if pin.isnumeric():
            key = key_from_pin(int(pin),len(binary_message))
        else:
            key = key_from_password(pin,len(binary_message))
    else:
        print()
        pin = input('Encryption Pin: ')
        print()
        if pin.isnumeric():
            key = key_from_pin(int(pin),len(binary_message))
        else:
            key = key_from_password(pin,len(binary_message))
    
    if algorithm == 'CBC':
        encrypted_binary = encrypt_binary_cipher_block_chaining(binary_message, key)
    else:
        encrypted_binary = encrypt_binary_stream_cipher(binary_message, key)
    
    encrypted_message = binary_to_message(encrypted_binary)
    
    if save_encrypted_message:
        message_to_file(encrypted_message,save_file_path)
    return encrypted_message

def decrypt_message(message=None, pin=None, algorithm='CBC', save_decrypted_message = False, save_file_path = 'decrypted_message.txt'):
    """    
    This funciton decrypts a 'message', not taken from a file. 
    It can then either print or save an derypted version of this message.
    
    If simply called as: 
    
    PyTextEncrypt.decrypt_message()
    
    the user will be prompted to input:
     
    message = the message to be decrypted
    pin = the decryption pin. Can be a numeric pin or alpha-numeric password.
    
    if save_decrypted_message is set True then the encrypted message will be 
    saved as a text file, at location save_file_path. 
    
    """
    
    if message != None:
        encrypted_binary = message_to_binary(message)
    else:
        print('Message to be decrypted: (When done press enter then control+D [mac] or control+Z [windows]). ')
        message = sys.stdin.read()
        print()
        encrypted_binary = message_to_binary(message)
        
    if pin != None:
        pin = str(pin)
        if pin.isnumeric():
            key = key_from_pin(int(pin),len(encrypted_binary))
        else:
            key = key_from_password(pin,len(encrypted_binary))
    else:
        print()
        pin = input('Encryption Pin: ')
        print()
        if pin.isnumeric():
            key = key_from_pin(int(pin),len(encrypted_binary))
        else:
            key = key_from_password(pin,len(encrypted_binary))
    
    if algorithm == 'CBC':
        decrypted_binary = decrypt_binary_cipher_block_chaining(encrypted_binary, key)
    else:
        decrypted_binary = decrypt_binary_stream_cipher(encrypted_binary, key)
    
    decrypted_message = binary_to_message(decrypted_binary)
    
    if save_decrypted_message:
        message_to_file(decrypted_message,save_file_path)
    return decrypted_message
 
def send_encrypted_email(your_email=None, their_email=None, subject='A message', pre_text='', post_text='', message_to_be_encrypted=None, pin = None):    
    """
    Encrypts a message with encrypt_message() and then sends it by email. 
    
    Only currently works for gmail. By default gmail will block pythons 
    attempts to log in to your gmail account, as it deems it insecure.
    
    To allow python access to your gmail, go to the following link
    https://myaccount.google.com/lesssecureapps
    and switch 'allow less secure apps' to ON. 
    
    """
    import smtplib, ssl
    import getpass
    
    port = 465
    smtp_server = "smtp.gmail.com"
    if your_email != None:
        sender_email = your_email
    else:
        sender_email = input('Sender email address: ')
    
    if sender_email[-10:] != '@gmail.com':
        print('TextEncryptorEmail only configured for gmail!')
        return 0
    
    password = getpass.getpass(prompt='Email password: ', stream=None)
    
    if their_email != None:
        reciever_email = their_email
    else:
        reciever_email = input('Reciever email address: ')

    
    encrypted_message = encrypt_message(message_to_be_encrypted, pin)
    
    message = ['Subject: '+subject,'\n',pre_text,'\n',encrypted_message,'\n',post_text]
    message = '\n'.join(message).encode('utf-8')
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server,port,context=context) as server:
        server.login(sender_email,password)
        server.sendmail(sender_email,reciever_email,message)
        print('Email sent.')


   
"""
The main mathematics behind the ciphers are governed by the properties
of the binary representations of integers and the XOR operation [+]. 
The binary representations of integers form a Group with operation [+]. 

Binary representation: 
Take two integers A and B

A = A_0 A_1 A_2 A_3 ...
B = B_0 B_1 B_2 B_3 ...

where A_i, B_i = {0, 1}, binary digits. 

The XOR operator is defined as acting on each digit 

A [+] B = (A_0 [+] B_0) (A_1 [+] B_1) (A_2 [+] B_2) ...

where: 

0 [+] 0 = 0
0 [+] 1 = 1             This is equivalent to 
1 [+] 0 = 1             X [+] Y = X + Y (mod 2).
1 [+] 1 = 0

Most of the ciphers fundamentally boil down to taking a plaintext 
P, converting it to a binary string, and then XORing that binary 
string with a 'key string' K, derived from a user-defined password. 
The result is a 'ciphertext' binary string C:
C = P [+] K.

which can then be converted back to alpha-numeric characters, the 
encrypted text. 

Note that this Group has an identity element, I = 00000000, which satisfies
A [+] I = A, and each element is its own inverse under the XOR operation:
A [+] A = I.  This means that for simple symmetric encryptions the same key
encrypts and decrypts the plaintext: 
C = P [+] K 
P = P [+] I = P [+] K [+] K = C [+] K

"""
    
# End.        
"""Although it would not normally be possible to crack a vignere cipher with so little ciphertext, 
in this case the plaintext of last sentence can be derived from hints provided - "Unveil the Truth, Unleash the infinite!"
is shown to the player several times - on the othello-rules page and after every othello game played. the presence
of punctuation helps draw notice to the end ciphertext being exactly the same format as that sentence.
This vignere cipher is also somewhat easier to crack because spaces and punctuation are not encrypted.
"""


from collections import Counter

#calculate how much a plains char was shifted when encrypted
def calculate_shift(plain_char, cipher_char):
    shift = (ord(cipher_char) - ord(plain_char)) % 26
    return shift

#find repeating patterns of shifts in the known ciphertext and return the most likely to be the key
def identify_repeating_key(ciphertext, plaintext):
    differences = [
        calculate_shift(p, c) 
        for p, c in zip(plaintext, ciphertext) 
        if p.isalpha() and c.isalpha()
    ]    
    
    for length in range(1, len(differences) + 1):
        pattern = differences[:length]
        repeated_pattern = pattern * (len(differences) // length) + pattern[:len(differences) % length]
        if repeated_pattern == differences:
            key = ''.join(chr(shift + ord('a')) for shift in pattern)
            return key
    
    key = ''.join(chr(shift + ord('a')) for shift in differences)
    return key

#extend key to full length of text
def generate_key(msg, key):
    key = list(key)
    if len(msg) == len(key):
        return "".join(key)
    else:
        for i in range(len(msg) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)

#decrypt the ciphertext using the key
def decrypt_vigenere_with_key(ciphertext, key):
    decrypted_text = []
    key = generate_key(ciphertext, key)  
    
    k=0
    for i in range(len(ciphertext)):
        char = ciphertext[i]
        # decrypt and increment key index only for alphabetic characters
        if char.isalpha():
            shift = ord(key[k].lower()) - ord('a')
            if char.isupper():
                decrypted_char = chr((ord(char) - shift - ord('A')) % 26 + ord('A'))
            else:
                decrypted_char = chr((ord(char) - shift - ord('a')) % 26 + ord('a'))
            decrypted_text.append(decrypted_char)
            k+=1
        else:
            decrypted_text.append(char)
    
    return ''.join(decrypted_text)

#once the longest repeating pattern is found - i.e. the letters of the key - 
#rearrage them in the correct order, found by finding the 1st known char that's % pattern length + 1
def reorder_pattern(pattern, ciphertext, known_plaintext):

    clean_cipher = ''.join(filter(str.isalpha, ciphertext))
    clean_known_plain = ''.join(filter(str.isalpha, known_plaintext))
    # Find the starting point in the ciphertext that corresponds to the start of the known plaintext
    start_index = len(clean_cipher) - len(clean_known_plain)
    
    # Calculate the offset in the pattern based on the start_index
    offset = start_index % len(pattern) + 1
    
    # Reorder the pattern
    reordered_pattern = pattern[offset:] + pattern[:offset]
    
    return reordered_pattern


#our case is:
ciphertext = "Eawpjyqox kofb uc zemx, uy jqej gnsx gn fw. Lnlriw ri nte zyamtrb gpx qel. Cgtyvt mfy Gznrb, Hvecufp mfy vvyghvbx!"
known_plaintext = "Unveil the Truth, Unleash the infinite!"
known_ciphertext = "Cgtyvt mfy Gznrb, Hvecufp mfy vvyghvbx!"


pattern = identify_repeating_key(known_ciphertext, known_plaintext)
reordered_key = reorder_pattern(pattern, ciphertext, known_plaintext)

decrypted_message = decrypt_vigenere_with_key(ciphertext, reordered_key)


print("Reordered Key:", reordered_key)
print("decrypted_message:", decrypted_message)
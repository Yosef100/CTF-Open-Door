#encrypt text using vignere cipher with key key
def vigenere_encrypt(plaintext, key):
    # Resulting encrypted text
    encrypted_text = []

    # Length of the key
    key_length = len(key)
    k= 0
    for i, char in enumerate(plaintext):
        # Encrypt and increment key index only for alphabetic characters 
        if char.isalpha():             
            shift = ord(key[k % key_length].lower()) - ord('a')
            if char.isupper():
                encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            elif char.islower():
                encrypted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            encrypted_text.append(encrypted_char)
            k+=1
            print (f"{char}, {encrypted_char}, {key[k % key_length]}, {ord(char)}, {ord(encrypted_char)}, shift: {shift}")
        else:
            
            # Non-alphabetic characters remain the same
            encrypted_text.append(char)

    return ''.join(encrypted_text)

plain = "Knowledge must be free, we will make it so. Spread to all beneath the sky. Unveil the Truth, Unleash the infinite!"
print(vigenere_encrypt(plain, "unity"))
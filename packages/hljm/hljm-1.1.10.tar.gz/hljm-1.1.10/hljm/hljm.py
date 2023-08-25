import random

# 解密函数
def decrypt_code(encrypted_code, decryption_key):
    decrypted_code = ""
    index = 0
    for char in encrypted_code:
        if index in decryption_key:
            decrypted_char = decryption_key[index]
            if decrypted_char == ' ':
                decrypted_code += ' ' * (encrypted_code[index + 1] == '密')
            else:
                decrypted_code += decrypted_char
        else:
            decrypted_code += char
        index += 1
    return decrypted_code

# 解密解密秘钥函数
def decrypt_decryption_key(encrypted_decryption_key):
    decryption_key = ""
    for char in encrypted_decryption_key:
        decrypted_char = chr(ord(char) - 1)
        decryption_key += decrypted_char
    return eval(decryption_key)

# 解密代码
def code_decryption(encrypted_code, encrypted_decryption_key):
    decryption_key = decrypt_decryption_key(encrypted_decryption_key)
    decrypted_code = decrypt_code(encrypted_code, decryption_key)
    return decrypted_code

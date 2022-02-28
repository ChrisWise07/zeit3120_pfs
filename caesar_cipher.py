from email import message


alphabet = "abcdefghijklmnopqrstuvwxyz"
enc_string = """
Ebiil, qefp fp x pbzobq jbppxdb!
"""

for cipher_shift in range(1, 26):
    enc_string = enc_string.lower()
    output_string = ""
    for character in enc_string:
        position_of_shifted_character = alphabet.find(character) - cipher_shift
        if character in alphabet:
            output_string += alphabet[position_of_shifted_character ]
        else:
            output_string += character
            
    print_message = f"""
You used a cipher shift of {str(cipher_shift)}
Your decrypted message reads:
{output_string}
"""

    print(print_message)
    

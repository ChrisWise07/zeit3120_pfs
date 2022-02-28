ciper_string = """
UZZF YTRNCGZZG VBYII. RMOI OI Y IALIRORAROZG ZT RNDR. UZZF BAVJ OG FNVZFOGU OR. BZZJ TZC RHZ BNRRNC HZCFI, RMCNN BNRRNC HZCFI YGF SMCYINI.
UZZF BAVJ. 
ROQ
"""

letter_map = {
    "a": "u",
    "b": "l",
    "c": "r",
    "d": "s",
    "e": "e",
    "f": "d",
    "g": "n",
    "h": "w",
    "i": "s",
    "j": "k",
    "k": "k",
    "l": "b",
    "m": "h",
    "n": "e",
    "o": "i",
    "p": "p",
    "q": "m",
    "r": "t",
    "s": "p",
    "t": "f",
    "u": "g",
    "v": "c",
    "w": "w",
    "x": "x",
    "y": "a",
    "z": "o",
    ".": ".",
    " ": " ",
    "\n": "\n",
    "," : ","
}

def letter_sub(cipher_string: str, letter_map: str):
    cipher_string = ciper_string.lower()
    new_string = ""
    for char in cipher_string:
        new_string += letter_map[char]
    return new_string

if __name__ == "__main__":
    new_string = letter_sub(ciper_string, letter_map )
    print(new_string)
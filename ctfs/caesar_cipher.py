import collections


alphabet = "abcdefghijklmnopqrstuvwxyz"

enc_string = """
pdeo eo w oaynap iaoowca!
"""

letterFrequency = {
    "e": 12.0,
    "t": 9.10,
    "a": 8.12,
    "o": 7.68,
    "i": 7.31,
    "n": 6.95,
    "s": 6.28,
    "r": 6.02,
    "h": 5.92,
    "d": 4.32,
    "l": 3.98,
    "u": 2.88,
    "c": 2.71,
    "m": 2.61,
    "f": 2.30,
    "y": 2.11,
    "w": 2.09,
    "g": 2.03,
    "p": 1.82,
    "b": 1.49,
    "v": 1.11,
    "k": 0.69,
    "x": 0.17,
    "q": 0.11,
    "j": 0.10,
    "z": 0.07,
}


def perform_all_cipher_shifts(enc_string: str):
    possible_plain_texts = []
    for cipher_shift in range(1, 26):
        enc_string = enc_string.lower()
        output_string = ""
        for character in enc_string:
            position_of_shifted_character = alphabet.find(character) - cipher_shift
            if character in alphabet:
                output_string += alphabet[position_of_shifted_character]
            else:
                output_string += character

        possible_plain_texts.append(output_string)

    return possible_plain_texts


def print_all_possible_shifts(enc_string: str):
    possible_plain_texts = perform_all_cipher_shifts(enc_string)
    for pos, string in enumerate(possible_plain_texts):
        print(
            f"""You used a cipher shift of {str(pos+1)} \nYour decrypted message reads: \n{string}\n"""
        )


def calculate_chi_squared(sentence: str):
    count_of_letters_in_sentence = collections.Counter(sentence)
    total_chi_squared = 0.0

    for char in alphabet:
        expected_number = (letterFrequency[char] / 100) * len(sentence)
        if char in count_of_letters_in_sentence:
            total_chi_squared += (
                (count_of_letters_in_sentence[char] - expected_number) ** 2
            ) / expected_number
        else:
            total_chi_squared += ((0 - expected_number) ** 2) / expected_number

    return total_chi_squared


def return_best_phrase(list_of_shifted_sentences: list):
    best_chi_squared, shifted_amount_for_best_score, best_sentence = float("inf"), 0, ""

    for shift_amount, sentence in enumerate(list_of_shifted_sentences):
        chi_squared_score = calculate_chi_squared(sentence)

        if chi_squared_score < best_chi_squared:
            best_chi_squared = chi_squared_score
            shifted_amount_for_best_score = shift_amount
            best_sentence = sentence

    return (best_sentence, shifted_amount_for_best_score)


def print_most_likely_shift(enc_string: str):
    best_phrase, shift_amount = return_best_phrase(
        perform_all_cipher_shifts(enc_string)
    )
    print(
        f"""The best cipher shift was {shift_amount+1} \nYour decrypted message reads: \n{best_phrase}\n"""
    )


if __name__ == "__main__":
    print("--- All Possible Shifts ---\n")
    print_all_possible_shifts(enc_string)
    print("\n--- Most Likely/Correct Shift ---\n")
    print_most_likely_shift(enc_string)

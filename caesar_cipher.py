import collections


alphabet = "abcdefghijklmnopqrstuvwxyz"

enc_string = """
pdeo eo w oaynap iaoowca!
"""

letterFrequency = {
    "E": 12.0,
    "T": 9.10,
    "A": 8.12,
    "O": 7.68,
    "I": 7.31,
    "N": 6.95,
    "S": 6.28,
    "R": 6.02,
    "H": 5.92,
    "D": 4.32,
    "L": 3.98,
    "U": 2.88,
    "C": 2.71,
    "M": 2.61,
    "F": 2.30,
    "Y": 2.11,
    "W": 2.09,
    "G": 2.03,
    "P": 1.82,
    "B": 1.49,
    "V": 1.11,
    "K": 0.69,
    "X": 0.17,
    "Q": 0.11,
    "J": 0.10,
    "Z": 0.07,
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
        expected_number = (letterFrequency[char.upper()] / 100) * len(sentence)
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
    possible_plain_texts = perform_all_cipher_shifts(enc_string)
    best_phrase, shift_amount = return_best_phrase(possible_plain_texts)
    print(
        f"""The best cipher shift was {shift_amount+1} \nYour decrypted message reads: \n{best_phrase}\n"""
    )


if __name__ == "__main__":
    print_all_possible_shifts(enc_string)
    print_most_likely_shift(enc_string)

from typing import Dict, List, Tuple
import numpy as np
import string
import re
import collections
from .utils import file_handler
from math import gcd

ASCII_OFFSET = ord("a")

"""
Source: 
http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
"""
ENGLISH_LETTER_FREQUENCIES = np.array(
    [
        8.12,
        1.49,
        2.71,
        4.32,
        12.0,
        2.3,
        2.03,
        5.92,
        7.31,
        0.1,
        0.69,
        3.98,
        2.61,
        6.95,
        7.68,
        1.82,
        0.11,
        6.02,
        6.28,
        9.1,
        2.88,
        1.11,
        2.09,
        0.17,
        2.11,
        0.07,
    ]
)

output_for_file = (
    "-----BEGIN VIGENERE KEY-----\n"
    "{key}\n"
    "-----END VIGENERE KEY-----\n\n"
    "-----BEGIN {mode} TEXT-----\n"
    "{text}\n"
    "-----END {mode} TEXT-----\n"
)


def convert_text_to_position_in_alphabet(text: str) -> np.ndarray:
    """
    Convert text to numbers.

    Args:
        text (str): The text to convert.

    Returns:
        list: A list of numbers each representing a letter's position in alphabet.
    """

    stripped_string = (
        re.sub(r"\s+", "", text)
        .lower()
        .translate(str.maketrans("", "", string.punctuation))
    )
    return np.array([ord(c) - ASCII_OFFSET for c in stripped_string])


def _recursive_shifted_row_coincidences_counter(
    encrypted_text: np.array,
    shifted_row: np.array,
    coincidence_count: np.array,
    current_index: int,
) -> np.array:
    """
    Count the number of times coincidences occur in encrypted text.

    Args:
        encrypted_text (np.array): The encrypted text to count coincidences in.
        shifted_row (np.array): The shifted row to count coincidences in.
        coincidence_count (np.array): A list of numbers each representing the
        number of coincidences for each shifted row.
        current_index (int): The number of times shifted_row has been shifted.
    
    Returns:
        np.array: A list of numbers each representing the
        number of coincidences for each shifted row.
    """
    if shifted_row.size:
        count = 0
        for pos, char in enumerate(shifted_row, start=1):
            if char == encrypted_text[current_index + pos]:
                count += 1

        coincidence_count[current_index] = count
        current_index += 1

        _recursive_shifted_row_coincidences_counter(
            encrypted_text=encrypted_text,
            shifted_row=shifted_row[:-1],
            coincidence_count=coincidence_count,
            current_index=current_index,
        )

    return coincidence_count


def count_shifted_coincidences(encrypted_text: np.array) -> np.array:
    """
    Count the number of times coincidences occur in encrypted text.

    Args:
        encrypted_text (np.array): The encrypted text to count coincidences in.

    Returns:
        np.array: A list of numbers each representing the
        number of coincidences for each shifted row.
    """
    return _recursive_shifted_row_coincidences_counter(
        encrypted_text=encrypted_text,
        shifted_row=encrypted_text[:-1],
        coincidence_count=np.zeros(encrypted_text.size - 1, dtype=np.int32),
        current_index=0,
    )


def key_length_counter(coincidence_count: np.array) -> Dict[int, int]:
    """
    Calculate gaps between high coincidence counts whilst
    recording the number of times gaps of that size have occur number times.

    Args:
        coincidence_count (np.array): A list of numbers each representing the
        number of coincidences for each shifted row.

    Returns:
        Dict[int, int]: A dictionary of likey key lengths mapped to
        appearance frequency.
    """
    min_large_count_limit = round(np.max(coincidence_count) - np.std(coincidence_count))
    count_of_possible_key_lengths = {}
    pos_previous_large_count = 0

    for pos, count in enumerate(coincidence_count):
        if count >= min_large_count_limit:
            if pos_previous_large_count:
                large_count_gap = pos - pos_previous_large_count
                if count_of_possible_key_lengths.get(large_count_gap):
                    count_of_possible_key_lengths[large_count_gap] += 1
                else:
                    count_of_possible_key_lengths[large_count_gap] = 1

            pos_previous_large_count = pos

    return count_of_possible_key_lengths


def sort_key_lengths(key_lengths: Dict[int, int]) -> List[int]:
    """
    Sort the key lengths.

    Args:
        key_lengths (Dict[int, int]): A dictionary of likey key lengths mapped to
        appearance frequency.

    Returns:
        List: A list of key lengths sort first by appearance frequency than length.
    """
    return [v[0] for v in sorted(key_lengths.items(), key=lambda kv: (-kv[1], kv[0]))]


def count_of_every_nth_letter(
    encrypted_text: np.array, n: int, start_index: int
) -> np.array:
    """
    Count the frequency of letters searching every nth letter.

    Args:
        encrypted_text (np.array): The text to count letters in.
        n (int): The nth letter to count.
        start_index (int): The start point to count from.

    Returns:
        np.array: A list of numbers each representing the frequency of the letter at the
        analgous index in alphabet (a=0, b=1, c=2, etc), when counting every nth letter.
    """
    letter_count = np.zeros((26,), dtype=np.int32)

    for char in encrypted_text[start_index::n]:
        letter_count[char] += 1

    return letter_count


def frequency_of_every_nth_letter(letter_count: np.ndarray) -> np.ndarray:
    """
    Calculate the frequency of every nth letter.

    Args:
        letter_count (np.array): A list of numbers each representing the frequency of
        the letter at the analgous index in alphabet (a=0, b=1, c=2, etc), when counting
        every nth letter.

    Returns:
        np.array: A list of numbers each representing the frequency of the letter at the
        analgous index in alphabet (a=0, b=1, c=2, etc), when counting every nth letter.
    """
    return letter_count / np.sum(letter_count)


def find_letter_in_key(
    frequency_of_every_nth_letter: np.array,
    expected_letter_frequency: np.array = ENGLISH_LETTER_FREQUENCIES,
) -> int:
    """
    Find the letter at the position in the key.

    Args:
        frequency_of_every_nth_letter (np.array): A list of numbers each representing the
        frequency of the letter at the analgous index in alphabet (a=0, b=1, c=2, etc), when
        counting every nth letter.
        key_length (int): The length of the key.
        start_index (int): The start point to count from.

    Returns:
        np.array: A list of numbers each representing the frequency of the letter at the
        analgous index in alphabet (a=0, b=1, c=2, etc), when counting every nth letter.
    """
    max_value = float("-inf")

    for shift in range(expected_letter_frequency.size):
        best_value = np.sum(frequency_of_every_nth_letter * expected_letter_frequency)
        if best_value > max_value:
            max_value = best_value
            best_shift = shift
        frequency_of_every_nth_letter = np.roll(frequency_of_every_nth_letter, -1)

    return best_shift


def find_possible_key(
    encrypted_text: np.ndarray,
    key_length: int,
) -> List[int]:
    """
    Find the possible key.

    Args:
        encrypted_text (np.array): The text to decrypt.
        key_length (int): The length of the key.

    Returns:
        np.array: A possible key.
    """
    return [
        find_letter_in_key(
            frequency_of_every_nth_letter(
                count_of_every_nth_letter(
                    encrypted_text=encrypted_text, n=key_length, start_index=pos
                )
            ),
        )
        for pos in range(key_length)
    ]


def find_all_possible_keys(encrypted_text: np.array) -> List[List[int]]:
    """
    Find all possible keys.

    Args:
        encrypted_text (np.array): The text to decrypt.

    Returns:
        List[List[int]]: A list of possible keys.
    """
    return [
        find_possible_key(encrypted_text, key_length)
        for key_length in key_length_counter(
            coincidence_count=count_shifted_coincidences(encrypted_text=encrypted_text)
        )
    ]


def remove_redundant_keys(possible_keys: List[List[int]]) -> List[List[int]]:
    """
    Remove redundant keys.

    Args:
        possible_keys (List[List[int]]): A list of possible keys.

    Returns:
        List[List[int]]: A list of possible keys without redundant keys.
    """
    copy_of_possible_keys = possible_keys.copy()

    for copy_key in copy_of_possible_keys:
        if copy_key in possible_keys:
            len_of_copy_key = len(copy_key)
            for other_key in copy_of_possible_keys:
                list_length_gcd = gcd(len_of_copy_key, len(other_key))
                if list_length_gcd > 1:
                    if other_key[list_length_gcd : list_length_gcd * 2] == copy_key:
                        possible_keys.remove(other_key)

    return possible_keys


def decrypt_text(encrypted_text: np.ndarray) -> Tuple[np.ndarray, List[List[int]]]:
    """
    Decrypt the text.

    Args:
        encrypted_text_as_nums: (np.array): The text to decrypt.
    Returns:
        np.array: The decrypted text.
    """
    possible_keys = remove_redundant_keys(find_all_possible_keys(encrypted_text))
    potential_solutions = np.empty(
        (len(possible_keys), encrypted_text.size), dtype=np.int32
    )

    for possible_key, potential_solution in zip(possible_keys, potential_solutions):
        for pos, char in enumerate(encrypted_text):
            potential_solution[pos] = (
                char - possible_key[pos % len(possible_key)]
            ) % 26

    return potential_solutions, possible_keys


def calculate_chi_squared(sentence: np.ndarray) -> float:
    """
    Calculate the chi squared value.

    Args:
        sentence (np.array): The sentence to calculate the chi squared value for.

    Returns:
        float: The chi squared value.
    """
    count_of_letters_in_sentence = collections.Counter(sentence)
    total_chi_squared = 0.0

    for pos, char_frequency in enumerate(ENGLISH_LETTER_FREQUENCIES):
        expected_number = (char_frequency / 100) * len(sentence)
        count_of_letter_in_sentence = int(count_of_letters_in_sentence[pos])
        total_chi_squared += (
            (count_of_letter_in_sentence - expected_number) ** 2
        ) / expected_number

    return total_chi_squared


def return_index_of_best_solution(list_of_sentences: np.ndarray) -> int:
    """
    Return the index of the best solution.

    Args:
        list_of_sentences (np.ndarray): The list of sentences to find the best key for.

    Returns:
        int: The index of the best key.
    """
    best_chi_squared, index_of_best_solution = float("inf"), 0

    for key_index, sentence in enumerate(list_of_sentences):
        chi_squared_score = calculate_chi_squared(sentence)

        if chi_squared_score < best_chi_squared:
            best_chi_squared = chi_squared_score
            index_of_best_solution = key_index

    return index_of_best_solution


def return_most_likely_key(encrypted_text: np.ndarray):
    """
    Return the most likely key. 

    Args:
        encrypted_text (np.ndarray): The text to decrypt.

    Returns:
        List[int]: The most likely key.
    """
    possible_solutions, possible_keys = decrypt_text(encrypted_text=encrypted_text)

    index_of_best_solution = return_index_of_best_solution(
        list_of_sentences=possible_solutions
    )

    return possible_keys[index_of_best_solution]


def apply_key_while_restoring_to_letters(
    text: np.ndarray, key: List[int], mode: int = -1
):
    """
    Apply the key to the text.
    
    Args:
        text (np.ndarray): The text to apply the key to.
        key (List[int]): The key to apply.
        mode (int): The mode -1 being decrypt, 1 being encrypt.

    Returns:
        np.ndarray: The text with the key applied.
"""
    len_key = len(key)
    return [
        chr(((char + mode * key[pos % len_key]) % 26) + ASCII_OFFSET)
        for pos, char in enumerate(text)
    ]


def restore_punctuation_to_string(
    original_string: str, modified_string: List[str]
) -> str:
    """
    Restore the punctuation to the original string.

    Args:
        original_encrypted_string (str): The original encrypted string.
        decrypted_string (List[str]): The decrypted string.

    Returns:
        str: The decrypted string with punctuation restored.
    """
    original_string = original_string.split()
    restored_string = ""

    for word in original_string:
        for char in word:
            if char.isalpha():
                if char.isupper():
                    restored_string += modified_string.pop(0).upper()
                else:
                    restored_string += modified_string.pop(0)
            else:
                restored_string += char
        restored_string += " "

    return restored_string.rstrip()


def key_to_string(key_as_alpha_pos: List[int]):
    """
    Convert the key to a string.

    Args:
        key_as_alpha_pos (List[int]): The key to convert.

    Returns:
        str: The key as a string.
    """
    key = ""
    for letter in key_as_alpha_pos:
        key += chr(letter + ASCII_OFFSET).upper()

    return key


def return_output_for_file(
    og_text: str,
    converted_text: np.ndarray,
    key: List[int],
    mode_as_word: str,
    mode_as_int: int,
):
    """
    Return the output for the file.

    Args:
        og_text (str): The original text.
        converted_text (np.ndarray): The converted text.
        key (List[int]): The key.
        mode_as_word (str): The mode as a word.
        mode_as_int (int): The mode as an int.

    Returns:
        str: The output for the file.
    """
    return output_for_file.format(
        key=key_to_string(key),
        mode=mode_as_word,
        text=restore_punctuation_to_string(
            original_string=og_text,
            modified_string=apply_key_while_restoring_to_letters(
                text=converted_text, key=key, mode=mode_as_int
            ),
        ),
    )


def vigenere_main(
    text: str, ofile: str, key: str = None, decode: bool = True, **kwargs
) -> None:
    """
    Main function for the vigenere cipher.

    Args:
        text (str): The text to encrypt or decrypt.
        ofile (str): The output file.
        key (str): The key to use.
        decode (bool): Whether to decode or not.
        **kwargs: The keyword arguments.

    Returns:
        None: None.
    """
    converted_text = convert_text_to_position_in_alphabet(text)

    if key:
        key = convert_text_to_position_in_alphabet(key)
    else:
        key = return_most_likely_key(encrypted_text=converted_text)

    if decode:
        output_for_file = return_output_for_file(
            og_text=text,
            converted_text=converted_text,
            key=key,
            mode_as_word="DECODED",
            mode_as_int=-1,
        )
    else:
        output_for_file = return_output_for_file(
            og_text=text,
            converted_text=converted_text,
            key=key,
            mode_as_word="ENCODED",
            mode_as_int=1,
        )

    if ofile:
        file_handler(path=ofile, mode="w", func=lambda f: f.write(output_for_file))
    else:
        print(output_for_file)

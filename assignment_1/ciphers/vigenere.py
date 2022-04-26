from typing import Dict, List
import numpy as np
import string
import re
from .utils import file_handler, output_for_file
from unidecode import unidecode
from warnings import warn

ASCII_OFFSET = ord("a")

"""
Source: 
https://www.sttmedia.com/characterfrequency-english
"""
ENGLISH_LETTER_FREQUENCIES = np.array(
    [
        0.0834,
        0.0154,
        0.0273,
        0.0414,
        0.126,
        0.0203,
        0.0192,
        0.0611,
        0.0671,
        0.0023,
        0.0087,
        0.0424,
        0.0253,
        0.068,
        0.077,
        0.0166,
        0.0009,
        0.0568,
        0.0611,
        0.0937,
        0.0285,
        0.0106,
        0.0234,
        0.002,
        0.0204,
        0.0006,
    ]
)

CHI_SQUARED_LIMIT = 1.00


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
        .translate(str.maketrans("", "", string.digits))
    )
    return np.array([ord(c) - ASCII_OFFSET for c in stripped_string])


def count_shifted_coincidences(encrypted_text: np.ndarray) -> np.ndarray:
    """
    Count the number of times coincidences occur in encrypted text.

    Args:
        encrypted_text (np.ndarray): The encrypted text to count coincidences in.

    Returns:
        np.ndarray: A list of numbers each representing the
        number of coincidences for each shifted row.
    """
    coincidence_count = np.zeros(encrypted_text.size - 1)
    shifted_row = encrypted_text[:-1]

    for n in range(1, len(encrypted_text)):
        count = 0

        for pos, char in enumerate(shifted_row):
            if char == encrypted_text[n + pos]:
                count += 1
        coincidence_count[n - 1] = count
        shifted_row = shifted_row[:-1]

    return coincidence_count


def key_length_counter(coincidence_count: np.ndarray) -> Dict[int, int]:
    """
    Calculate gaps between high coincidence counts whilst
    recording the number of times gaps of that size have occured.

    Args:
        coincidence_count (np.ndarray): A list of numbers each representing the
        number of coincidences for each shifted row.

    Returns:
        Dict[int, int]: A dictionary of likey key lengths mapped to
        appearance frequency.
    """
    count_of_possible_key_lengths = {}
    pos_previous_large_count = 0

    for pos, count in enumerate(coincidence_count):
        min_large_count_limit = 4.0 * (len(coincidence_count) - pos) * (1 / 52)
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


def prune_possible_keys(sorted_key_lengths: List[int]) -> List[int]:
    """
    Prune the possible key lengths.

    Args:
        sort_keys (List[int]): A list of key lengths sorted first by appearance frequency than length.

    Returns:
        List: A list of key lengths pruned.
    """
    list_to_check = sorted_key_lengths[1:]
    element_number = 0

    while len(list_to_check):
        key_length = sorted_key_lengths[element_number]
        for other_key_length in list_to_check:
            if other_key_length % key_length == 0:
                sorted_key_lengths.remove(other_key_length)
        element_number += 1
        list_to_check = sorted_key_lengths[element_number + 1 :]

    return sorted_key_lengths


def count_of_every_nth_letter(
    encrypted_text: np.ndarray, n: int, start_index: int
) -> np.ndarray:
    """
    Count the frequency of letters searching every nth letter.

    Args:
        encrypted_text (np.ndarray): The text to count letters in.
        n (int): The nth letter to count.
        start_index (int): The start point to count from.

    Returns:
        np.ndarray: A list of numbers each representing the frequency of the letter at the
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
        letter_count (np.ndarray): A list of numbers each representing the frequency of
        the letter at the analgous index in alphabet (a=0, b=1, c=2, etc), when counting
        every nth letter.

    Returns:
        np.ndarray: A list of numbers each representing the frequency of the letter at the
        analgous index in alphabet (a=0, b=1, c=2, etc), when counting every nth letter.
    """
    return letter_count / np.sum(letter_count)


def find_letter_in_key(
    frequency_of_every_nth_letter: np.ndarray,
    expected_letter_frequency: np.ndarray = ENGLISH_LETTER_FREQUENCIES,
) -> int:
    """
    Find the letter at the position in the key.

    Args:
        frequency_of_every_nth_letter (np.ndarray): A list of numbers each representing the
        frequency of the letter at the analgous index in alphabet (a=0, b=1, c=2, etc), when
        counting every nth letter.
        key_length (int): The length of the key.
        start_index (int): The start point to count from.

    Returns:
        np.ndarray: A list of numbers each representing the frequency of the letter at the
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
        encrypted_text (np.ndarray): The text to decrypt.
        key_length (int): The length of the key.

    Returns:
        np.ndarray: A possible key.
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


def return_solution_for_key(key: List[int], encrypted_text: np.ndarray) -> np.ndarray:
    """
    Return the solution for the key.

    Args:
        key (List[int]): The key for decryption.
        encrypted_text (np.ndarray): The text to decrypt.

    Returns:
        np.ndarray: The decrypted text as array of numbers representing letter
        position in alphabet.
    """
    potential_solution = np.empty((encrypted_text.size,), dtype=np.uint8)

    for pos, char in enumerate(encrypted_text):
        potential_solution[pos] = (char - key[pos % len(key)]) % 26

    return potential_solution


def calculate_chi_squared(sentence: np.ndarray) -> float:
    """
    Calculate the chi squared value.

    Args:
        sentence (np.ndarray): The sentence to calculate the chi squared value for.

    Returns:
        float: The chi squared value.
    """
    observed_frequency = np.bincount(sentence, minlength=26)
    expected_frequency = ENGLISH_LETTER_FREQUENCIES * sentence.size
    return np.sum(
        np.square(observed_frequency - expected_frequency) / expected_frequency
    )


def return_sorted_possible_key_lengths(
    encrypted_text: np.ndarray,
) -> List[int]:
    """
    Return the possible key lengths.

    Args:
        encrypted_text (np.ndarray): The text to decrypt.

    Returns:
        List[int]: The possible key lengths.
    """
    return sort_key_lengths(
        key_length_counter(
            coincidence_count=count_shifted_coincidences(encrypted_text=encrypted_text)
        )
    )


def return_best_key(encrypted_text: np.ndarray):
    """
    Return the most likely key.

    Args:
        encrypted_text (np.ndarray): The text to decrypt.

    Returns:
        List[int]: The best key.
    """
    best_chi_squared = float("inf")

    for possible_key_length in prune_possible_keys(
        return_sorted_possible_key_lengths(encrypted_text)
    ):
        possible_key = find_possible_key(
            encrypted_text=encrypted_text, key_length=possible_key_length
        )

        possible_solution = return_solution_for_key(
            key=possible_key, encrypted_text=encrypted_text
        )

        chi_squared_score = calculate_chi_squared(sentence=possible_solution)

        if (chi_squared_score / len(encrypted_text)) < CHI_SQUARED_LIMIT:
            return possible_key

        if chi_squared_score < best_chi_squared:
            best_chi_squared = chi_squared_score
            best_key = possible_key

    return best_key


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
        np.ndarray: The text with the key applied."""
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
    original_string = re.findall(r"\S+|\n", original_string)
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
        key += chr(letter + ASCII_OFFSET)

    return key.upper()


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
        cipher="VIGENERE",
        key=key_to_string(key),
        mode=mode_as_word,
        text=restore_punctuation_to_string(
            original_string=og_text,
            modified_string=apply_key_while_restoring_to_letters(
                text=converted_text, key=key, mode=mode_as_int
            ),
        ),
    )


def replace_non_ascii_with_alike_char(text: str) -> str:
    """
    Replace non-ascii characters with a similar character.

    Args:
        text (str): The text to replace non-ascii characters in.

    Returns:
        str: The text with non-ascii characters replaced.
    """
    warn(
        "Non-Enlgish character detected. Vigenere cipher currently works only "
        "with ASCII/English text. All non-English characters will be replaced "
        "with an alike representation.",
    )
    return unidecode(text)


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

    if not (text.isascii()):
        text = replace_non_ascii_with_alike_char(text)

    converted_text = convert_text_to_position_in_alphabet(text)

    if key is not None:
        if not (key.isascii()):
            key = replace_non_ascii_with_alike_char(key)
        key = convert_text_to_position_in_alphabet(key)
    else:
        key = return_best_key(encrypted_text=converted_text)

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

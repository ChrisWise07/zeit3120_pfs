from ast import Lambda
from typing import Callable, Dict
import unittest
from unittest import result
import numpy as np
import os
from ciphers.utils import file_handler
from ciphers.vigenere import (
    convert_text_to_position_in_alphabet,
    count_shifted_coincidences,
    key_length_counter,
    sort_key_lengths,
    count_of_every_nth_letter,
    frequency_of_every_nth_letter,
    find_letter_in_key,
    decrypt_text,
    find_possible_key,
    find_all_possible_keys,
    decrypt_text,
    return_index_of_best_solution,
    return_most_likely_key,
    restore_punctuation_to_string,
    vigenere_main,
    apply_key_while_restoring_to_letters,
    remove_redundant_keys,
)

brown_fox_text = "The quick brown fox \njumps over the lazy dog!"
brown_fox_text_position_in_alphabet = [
    19,
    7,
    4,
    16,
    20,
    8,
    2,
    10,
    1,
    17,
    14,
    22,
    13,
    5,
    14,
    23,
    9,
    20,
    12,
    15,
    18,
    14,
    21,
    4,
    17,
    19,
    7,
    4,
    11,
    0,
    25,
    24,
    3,
    14,
    6,
]

test_phrase = "At seventeen minutes past four in the afternoon, whilst the passengers were assembled at lunch in the great saloon, a slight shock was felt on the hull of the Scotia"
test_phrase_encrypted = "Kx qozcxxcor ksrsdiq zeqd jmev gx xfo eddipxsmx, afspqd xfo tycwcxkcbw uovc kwqoqzvib kx jerar ml dlc qvckx qkpmyr, y cpgqlr clmmo ukw dopr yr rri fepj yj rri Qmsrse"
test_phrase_as_list = [
    "a",
    "t",
    "s",
    "e",
    "v",
    "e",
    "n",
    "t",
    "e",
    "e",
    "n",
    "m",
    "i",
    "n",
    "u",
    "t",
    "e",
    "s",
    "p",
    "a",
    "s",
    "t",
    "f",
    "o",
    "u",
    "r",
    "i",
    "n",
    "t",
    "h",
    "e",
    "a",
    "f",
    "t",
    "e",
    "r",
    "n",
    "o",
    "o",
    "n",
    "w",
    "h",
    "i",
    "l",
    "s",
    "t",
    "t",
    "h",
    "e",
    "p",
    "a",
    "s",
    "s",
    "e",
    "n",
    "g",
    "e",
    "r",
    "s",
    "w",
    "e",
    "r",
    "e",
    "a",
    "s",
    "s",
    "e",
    "m",
    "b",
    "l",
    "e",
    "d",
    "a",
    "t",
    "l",
    "u",
    "n",
    "c",
    "h",
    "i",
    "n",
    "t",
    "h",
    "e",
    "g",
    "r",
    "e",
    "a",
    "t",
    "s",
    "a",
    "l",
    "o",
    "o",
    "n",
    "a",
    "s",
    "l",
    "i",
    "g",
    "h",
    "t",
    "s",
    "h",
    "o",
    "c",
    "k",
    "w",
    "a",
    "s",
    "f",
    "e",
    "l",
    "t",
    "o",
    "n",
    "t",
    "h",
    "e",
    "h",
    "u",
    "l",
    "l",
    "o",
    "f",
    "t",
    "h",
    "e",
    "s",
    "c",
    "o",
    "t",
    "i",
    "a",
]
test_phrase_encrypted_as_list = [
    "k",
    "x",
    "q",
    "o",
    "z",
    "c",
    "x",
    "x",
    "c",
    "o",
    "r",
    "k",
    "s",
    "r",
    "s",
    "d",
    "i",
    "q",
    "z",
    "e",
    "q",
    "d",
    "j",
    "m",
    "e",
    "v",
    "g",
    "x",
    "x",
    "f",
    "o",
    "e",
    "d",
    "d",
    "i",
    "p",
    "x",
    "s",
    "m",
    "x",
    "a",
    "f",
    "s",
    "p",
    "q",
    "d",
    "x",
    "f",
    "o",
    "t",
    "y",
    "c",
    "w",
    "c",
    "x",
    "k",
    "c",
    "b",
    "w",
    "u",
    "o",
    "v",
    "c",
    "k",
    "w",
    "q",
    "o",
    "q",
    "z",
    "v",
    "i",
    "b",
    "k",
    "x",
    "j",
    "e",
    "r",
    "a",
    "r",
    "m",
    "l",
    "d",
    "l",
    "c",
    "q",
    "v",
    "c",
    "k",
    "x",
    "q",
    "k",
    "p",
    "m",
    "y",
    "r",
    "y",
    "c",
    "p",
    "g",
    "q",
    "l",
    "r",
    "c",
    "l",
    "m",
    "m",
    "o",
    "u",
    "k",
    "w",
    "d",
    "o",
    "p",
    "r",
    "y",
    "r",
    "r",
    "r",
    "i",
    "f",
    "e",
    "p",
    "j",
    "y",
    "j",
    "r",
    "r",
    "i",
    "q",
    "m",
    "s",
    "r",
    "s",
    "e",
]
default_err_msg = "{} has not returned correct output"
test_decoded_output_file = (
    f"-----BEGIN VIGENERE KEY-----\n"
    f"KEY\n"
    f"-----END VIGENERE KEY-----\n\n"
    f"-----BEGIN DECODED TEXT-----\n"
    f"{test_phrase}\n"
    f"-----END DECODED TEXT-----\n"
)
test_encoded_output_file = (
    f"-----BEGIN VIGENERE KEY-----\n"
    f"KEY\n"
    f"-----END VIGENERE KEY-----\n\n"
    f"-----BEGIN ENCODED TEXT-----\n"
    f"{test_phrase_encrypted}\n"
    f"-----END ENCODED TEXT-----\n"
)
root_directory = os.getcwd()
test_encoded_text = file_handler(
    path=os.path.join(root_directory, "test/sample_text/vigenere_encoded_text.txt"),
    mode="r",
    func=lambda f: f.read(),
)


class vigenere_tester(unittest.TestCase):
    def numpy_array_equality_tester(
        self,
        func: Callable,
        func_kwargs: Dict[str, any],
        expected_array: np.array,
        err_message: str,
    ) -> None:
        with self.subTest(err_message):
            (
                np.testing.assert_allclose(
                    func(**func_kwargs), expected_array, rtol=1e-03
                ),
                None,
            )

    def test_text_is_converted_correctly(self):
        self.numpy_array_equality_tester(
            func=convert_text_to_position_in_alphabet,
            func_kwargs={"text": "abc"},
            expected_array=np.array([0, 1, 2]),
            err_message="Text has not converted correctly for abc example",
        )

        self.numpy_array_equality_tester(
            func=convert_text_to_position_in_alphabet,
            func_kwargs={"text": brown_fox_text},
            expected_array=np.array(brown_fox_text_position_in_alphabet),
            err_message="Text has not converted correctly for brown fox example",
        )

    def test_count_shifted_coincidences(self):
        self.numpy_array_equality_tester(
            func=count_shifted_coincidences,
            func_kwargs={
                "encrypted_text": convert_text_to_position_in_alphabet(
                    text="vvhqwvvrmhusgjg"
                )
            },
            expected_array=np.array([2, 1, 0, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0]),
            err_message=default_err_msg.format("Counted shifted coincidences"),
        )

    def test_key_length_counter(self):
        coincidence_count = count_shifted_coincidences(
            encrypted_text=(
                convert_text_to_position_in_alphabet(text=test_phrase_encrypted)
            )
        )

        self.assertEqual(
            key_length_counter(coincidence_count=coincidence_count),
            {4: 1, 6: 2, 3: 2, 24: 1},
            default_err_msg.format("Key length counter"),
        )

    def test_count_of_every_nth_letter(self):
        self.numpy_array_equality_tester(
            func=count_of_every_nth_letter,
            func_kwargs={
                "encrypted_text": convert_text_to_position_in_alphabet(
                    text="ABAABCCACBBC"
                ),
                "n": 4,
                "start_index": 0,
            },
            expected_array=np.array(
                [
                    1,
                    1,
                    1,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ]
            ),
            err_message=default_err_msg.format("Count of every nth letter"),
        )

    def test_frequency_of_every_nth_letter(self):
        self.numpy_array_equality_tester(
            func=frequency_of_every_nth_letter,
            func_kwargs={
                "letter_count": count_of_every_nth_letter(
                    encrypted_text=convert_text_to_position_in_alphabet(
                        text="ABAABCCACBBC"
                    ),
                    n=4,
                    start_index=0,
                ),
            },
            expected_array=np.array(
                [
                    0.3333,
                    0.3333,
                    0.3333,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ]
            ),
            err_message=default_err_msg.format("Freq of every nth letter"),
        )

    def test_find_letter_at_position_in_key(self):
        self.assertEqual(
            find_letter_in_key(
                frequency_of_every_nth_letter=np.array([0.25, 0.625, 0.125]),
                expected_letter_frequency=np.array([0.1, 0.2, 0.7]),
            ),
            2,
            default_err_msg.format("Find letter at position in key"),
        )

    def test_find_possible_key(self):
        self.assertEqual(
            find_possible_key(
                encrypted_text=convert_text_to_position_in_alphabet(
                    text=test_phrase_encrypted
                ),
                key_length=3,
            ),
            [10, 4, 24],
            default_err_msg.format("Find possible key"),
        )

    def test_find_all_possible_keys(self):
        result = find_all_possible_keys(
            encrypted_text=convert_text_to_position_in_alphabet(
                text=test_phrase_encrypted
            ),
        )
        self.assertEqual(
            result[2],
            [10, 4, 24],
            default_err_msg.format("Find all possible keys"),
        )
        self.assertEqual(
            len(result),
            4,
            default_err_msg.format("Find all possible keys"),
        )

    def test_remove_redundant_keys(self):
        self.assertEqual(
            remove_redundant_keys(
                [
                    [10, 4, 26, 27],
                    [10, 4, 24],
                    [10, 4, 24] * 2,
                    [10, 4, 24] * 3,
                ],
            ),
            [[10, 4, 26, 27], [10, 4, 24]],
            default_err_msg.format("Remove redundant keys"),
        )

    def test_decrypt_text(self):
        potential_solutions, possible_keys = decrypt_text(
            encrypted_text=convert_text_to_position_in_alphabet(
                text=test_phrase_encrypted
            )
        )
        self.assertEqual(
            len(potential_solutions[0]), 134, default_err_msg.format("Decrypt text")
        )
        self.assertEqual(
            len(potential_solutions), 3, default_err_msg.format("Decrypt text")
        )

    def test_return_index_of_best_key(self):
        potential_solutions, possible_keys = decrypt_text(
            encrypted_text=convert_text_to_position_in_alphabet(
                text=test_phrase_encrypted
            )
        )
        best_key = return_index_of_best_solution(list_of_sentences=potential_solutions)
        self.assertEqual(
            best_key, 1, default_err_msg.format("Return index of best key")
        )

    def test_solve_vigenere(self):
        key = return_most_likely_key(
            encrypted_text=convert_text_to_position_in_alphabet(
                text=test_phrase_encrypted
            )
        )
        self.assertEqual(key, [10, 4, 24], default_err_msg.format("Solve vigenere"))

    def test_apply_key_while_restoring_to_letters_decryption(self):
        result = apply_key_while_restoring_to_letters(
            text=convert_text_to_position_in_alphabet(text=test_phrase_encrypted),
            key=[10, 4, 24],
        )
        self.assertEqual(
            result,
            test_phrase_as_list,
            default_err_msg.format("apply_key_while_restoring_to_letters"),
        )

    def test_apply_key_while_restoring_to_letters_encryption(self):
        result = apply_key_while_restoring_to_letters(
            text=convert_text_to_position_in_alphabet(text=test_phrase),
            key=[10, 4, 24],
            mode=1,
        )
        self.assertEqual(
            result,
            test_phrase_encrypted_as_list,
            default_err_msg.format("apply_key_while_restoring_to_letters"),
        )

    def test_restore_punctuation_to_string(self):
        self.assertEqual(
            restore_punctuation_to_string(
                original_string=test_phrase_encrypted,
                modified_string=test_phrase_as_list,
            ),
            test_phrase,
            default_err_msg.format("Restore punctuation to string"),
        )

    def test_main_decoding_unknown_key(self):
        vigenere_main(
            text=test_phrase_encrypted,
            ofile=os.path.join(
                root_directory, "test/sample_text/vigenere_decoded_text.txt"
            ),
        )

        with open(
            os.path.join(root_directory, "test/sample_text/vigenere_decoded_text.txt"),
            "r",
        ) as decoded_file:
            decoded_text = decoded_file.read()
            self.assertEqual(
                decoded_text, test_decoded_output_file, default_err_msg.format("Main")
            )

    def test_main_decoding_known_key(self):
        vigenere_main(
            text=test_phrase_encrypted,
            ofile=os.path.join(
                root_directory, "test/sample_text/vigenere_decoded_text.txt"
            ),
            key="KEY",
        )

        with open(
            os.path.join(root_directory, "test/sample_text/vigenere_decoded_text.txt"),
            "r",
        ) as decoded_file:
            decoded_text = decoded_file.read()
            self.assertEqual(
                decoded_text, test_decoded_output_file, default_err_msg.format("Main")
            )

    def test_main_encoding(self):
        vigenere_main(
            text=test_phrase,
            ofile=os.path.join(
                root_directory, "test/sample_text/vigenere_encoded_text_from_test.txt"
            ),
            key="KEY",
            decode=False,
        )

        with open(
            os.path.join(
                root_directory, "test/sample_text/vigenere_encoded_text_from_test.txt"
            ),
            "r",
        ) as encoded_file:
            encoded_text = encoded_file.read()
            self.assertEqual(
                encoded_text, test_encoded_output_file, default_err_msg.format("Main")
            )


if __name__ == "__main__":
    unittest.main()

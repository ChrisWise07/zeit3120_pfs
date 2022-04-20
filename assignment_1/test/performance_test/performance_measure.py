import os
import sys
import numpy as np
import time
from typing import Callable, Dict

root_folder = os.path.abspath(__file__)
for i in range(3):
    root_folder = os.path.dirname(root_folder)
sys.path.append(root_folder)

from main import main

NUM_OF_TESTS = 25


def abstract_tester(
    test_func: Callable, test_kwargs: Dict[str, any], test_name: str = ""
) -> None:
    run_time = np.empty(NUM_OF_TESTS, dtype=np.float64)
    for i in range(NUM_OF_TESTS):
        begin_time = time.time()
        test_func(**test_kwargs)
        run_time[i] = time.time() - begin_time
    print(f"Average run time in seconds {test_name}: {np.mean(run_time):.4f}")


def vigenere_different_length_key_encoding_tester():
    key_lengths = {3, 6, 12}
    for key_length in key_lengths:
        abstract_tester(
            test_func=main,
            test_kwargs={
                "args": [
                    "--ifile",
                    os.path.join(
                        root_folder,
                        "test/performance_test/plaintext/1000_words_plaintext.txt",
                    ),
                    "--ofile",
                    os.path.join(
                        root_folder,
                        f"test/performance_test/ciphertext/1000_words_ciphertext_vigenere_{key_length}_letter_key.txt",
                    ),
                    "--decode",
                    False,
                    "--cipher",
                    "vigenere",
                    "--key",
                    os.path.join(
                        root_folder,
                        f"test/performance_test/keys/{key_length}_letter_key.txt",
                    ),
                ]
            },
            test_name=f"for Vigenere encoding with {key_length} letter key",
        )


def vigenere_different_plaintext_length_encoding_tester():
    factor = 100
    plaintext_lengths = {1 * factor, 10 * factor, 100 * factor}
    for plaintext_length in plaintext_lengths:
        abstract_tester(
            test_func=main,
            test_kwargs={
                "args": [
                    "--ifile",
                    os.path.join(
                        root_folder,
                        f"test/performance_test/plaintext/{plaintext_length}_words_plaintext.txt",
                    ),
                    "--ofile",
                    os.path.join(
                        root_folder,
                        f"test/performance_test/ciphertext/{plaintext_length}_words_ciphertext_vigenere_6_letter_key.txt",
                    ),
                    "--decode",
                    False,
                    "--cipher",
                    "vigenere",
                    "--key",
                    os.path.join(
                        root_folder,
                        f"test/performance_test/keys/6_letter_key.txt",
                    ),
                ]
            },
            test_name=f"for Vigenere encoding with 6 letter key for {plaintext_length} words plaintext",
        )


def vigenere_different_length_key_decoding_known_key_tester():
    key_lengths = {3, 6, 12}
    for key_length in key_lengths:
        abstract_tester(
            test_func=main,
            test_kwargs={
                "args": [
                    "--ifile",
                    os.path.join(
                        root_folder,
                        f"test/performance_test/ciphertext/{key_length}_letter_key_vigenere_encrypted_text.txt",
                    ),
                    "--ofile",
                    os.path.join(
                        root_folder,
                        f"test/performance_test/decrypted_plaintext/{key_length}_letter_key_vigenere_decrypted_text.txt",
                    ),
                    "--cipher",
                    "vigenere",
                    "--key",
                    os.path.join(
                        root_folder,
                        f"test/performance_test/keys/{key_length}_letter_key.txt",
                    ),
                ]
            },
            test_name=f"for Vigenere decoding known key with {key_length} letter key",
        )


def vigenere_different_plaintext_length_decoding_known_key_tester():
    factor = 100
    plaintext_lengths = {1 * factor, 10 * factor, 100 * factor}
    for plaintext_length in plaintext_lengths:
        abstract_tester(
            test_func=main,
            test_kwargs={
                "args": [
                    "--ifile",
                    os.path.join(
                        root_folder,
                        f"test/performance_test/ciphertext/{plaintext_length}_words_vigenere_encrypted_text.txt",
                    ),
                    "--ofile",
                    os.path.join(
                        root_folder,
                        f"test/performance_test/decrypted_plaintext/{plaintext_length}_vigenere_decrypted_text.txt",
                    ),
                    "--cipher",
                    "vigenere",
                    "--key",
                    os.path.join(
                        root_folder,
                        f"test/performance_test/keys/6_letter_key.txt",
                    ),
                ]
            },
            test_name=f"for Vigenere decoding known 6 letter key for {plaintext_length} words plaintext",
        )


def vigenere_different_length_key_decoding_unknown_key_tester():
    key_lengths = {3, 6, 12}
    for key_length in key_lengths:
        abstract_tester(
            test_func=main,
            test_kwargs={
                "args": [
                    "--ifile",
                    os.path.join(
                        root_folder,
                        f"test/performance_test/ciphertext/{key_length}_letter_key_vigenere_encrypted_text.txt",
                    ),
                    "--ofile",
                    os.path.join(
                        root_folder,
                        f"test/performance_test/decrypted_plaintext/{key_length}_letter_key_vigenere_decrypted_text.txt",
                    ),
                    "--cipher",
                    "vigenere",
                ]
            },
            test_name=f"for Vigenere decoding unknown key with {key_length} letter key",
        )


def vigenere_different_plaintext_length_decoding_unknown_key_tester():
    factor = 100
    plaintext_lengths = {1 * factor, 10 * factor, 100 * factor}
    for plaintext_length in plaintext_lengths:
        abstract_tester(
            test_func=main,
            test_kwargs={
                "args": [
                    "--ifile",
                    os.path.join(
                        root_folder,
                        f"test/performance_test/ciphertext/{plaintext_length}_words_vigenere_encrypted_text.txt",
                    ),
                    "--ofile",
                    os.path.join(
                        root_folder,
                        f"test/performance_test/ciphertext/{plaintext_length}_vigenere_decrypted_text.txt",
                    ),
                    "--cipher",
                    "vigenere",
                ]
            },
            test_name=f"for Vigenere decoding unknown 6 letter key for {plaintext_length} words plaintext",
        )


def feistel_different_length_key_encoding_decoding_tester():
    key_lengths = {6}
    for key_length in key_lengths:
        abstract_tester(
            test_func=main,
            test_kwargs={
                "args": [
                    "--ifile",
                    os.path.join(
                        root_folder,
                        "test/performance_test/plaintext/100_words_plaintext.txt",
                    ),
                    "--ofile",
                    os.path.join(
                        root_folder,
                        f"test/performance_test/ciphertext/100_words_feistel_encrypted_text.txt",
                    ),
                    "--decode",
                    False,
                    "--cipher",
                    "feistel",
                    "--key",
                    os.path.join(
                        root_folder,
                        f"test/performance_test/keys/{key_length}_letter_key.txt",
                    ),
                ]
            },
            test_name=f"for Feistel encoding/decoding with {key_length} letter key",
        )


def feistel_different_plaintext_length_decoding_known_key_tester():
    factor = 100
    plaintext_lengths = {1 * factor, 10 * factor, 100 * factor}
    for plaintext_length in plaintext_lengths:
        abstract_tester(
            test_func=main,
            test_kwargs={
                "args": [
                    "--ifile",
                    os.path.join(
                        root_folder,
                        f"test/performance_test/ciphertext/{plaintext_length}_words_feistel_encrypted_text.txt",
                    ),
                    "--ofile",
                    os.path.join(
                        root_folder,
                        f"test/performance_test/decrypted_plaintext/{plaintext_length}_feistel_decrypted_text.txt",
                    ),
                    "--cipher",
                    "feistel",
                    "--key",
                    os.path.join(
                        root_folder,
                        f"test/performance_test/keys/6_letter_key.txt",
                    ),
                ]
            },
            test_name=f"for Feistel decoding/encoding known 6 letter key for {plaintext_length} words plaintext",
        )


if __name__ == "__main__":
    globals()[sys.argv[1]]()

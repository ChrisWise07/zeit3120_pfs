from base64 import encode
import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py"))
from main import main
from ciphers.utils import file_handler

root_directory = os.getcwd()
test_phrase = "At seventeen minutes past four in the afternoon, whilst the passengers were assembled at lunch in the great saloon, a slight shock was felt on the hull of the Scotia"
test_phrase_encrypted = "Kx qozcxxcor ksrsdiq zeqd jmev gx xfo eddipxsmx, afspqd xfo tycwcxkcbw uovc kwqoqzvib kx jerar ml dlc qvckx qkpmyr, y cpgqlr clmmo ukw dopr yr rri fepj yj rri Qmsrse"
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
default_err_msg = "{} has not returned correct output"


class feistel_tester(unittest.TestCase):
    def test_main_encode_vigenere(self):
        main(
            args=[
                "--ifile",
                os.path.join(
                    root_directory,
                    "test/sample_text/vigenere_decoded_text_for_test.txt",
                ),
                "--ofile",
                os.path.join(
                    root_directory, "test/sample_text/vigenere_encoded_text.txt"
                ),
                "--decode",
                False,
                "--cipher",
                "vigenere",
                "--key",
                os.path.join(root_directory, "test/sample_text/key.txt"),
            ]
        )
        encoded_text = file_handler(
            path=os.path.join(
                root_directory, "test/sample_text/vigenere_encoded_text.txt"
            ),
            mode="r",
            func=lambda f: f.read(),
        )
        self.assertEqual(
            encoded_text,
            test_encoded_output_file,
            default_err_msg.format("main_encode_vigenere"),
        )

    def test_main_decode_unknown_key_vigenere(self):
        main(
            args=[
                "--ifile",
                os.path.join(
                    root_directory,
                    "test/sample_text/vigenere_encoded_text_for_test.txt",
                ),
                "--ofile",
                os.path.join(
                    root_directory, "test/sample_text/vigenere_encoded_text.txt"
                ),
                "--cipher",
                "vigenere",
            ]
        )
        decoded_text = file_handler(
            path=os.path.join(
                root_directory, "test/sample_text/vigenere_decoded_text.txt"
            ),
            mode="r",
            func=lambda f: f.read(),
        )
        self.assertEqual(
            decoded_text,
            test_decoded_output_file,
            default_err_msg.format("main_decode_unknown_key_vigenere"),
        )

    def test_main_decode_known_key_vigenere(self):
        main(
            args=[
                "--ifile",
                os.path.join(
                    root_directory,
                    "test/sample_text/vigenere_encoded_text_for_test.txt",
                ),
                "--ofile",
                os.path.join(
                    root_directory, "test/sample_text/vigenere_encoded_text.txt"
                ),
                "--cipher",
                "vigenere",
                "--key",
                os.path.join(root_directory, "test/sample_text/key.txt"),
            ]
        )
        decoded_text = file_handler(
            path=os.path.join(
                root_directory, "test/sample_text/vigenere_decoded_text.txt"
            ),
            mode="r",
            func=lambda f: f.read(),
        )
        self.assertEqual(
            decoded_text,
            test_decoded_output_file,
            default_err_msg.format("main_decode_unknown_key_vigenere"),
        )

    def test_main_no_input_file_raises_error(self):
        self.assertRaises(
            ValueError,
            main,
            args=[
                "--ofile",
                os.path.join(
                    root_directory, "test/sample_text/vigenere_encoded_text.txt"
                ),
                "--cipher",
                "vigenere",
                "--key",
                os.path.join(root_directory, "test/sample_text/key.txt"),
            ],
        )

    def test_main_invalid_input_file_path_raises_error(self):
        self.assertRaises(
            ValueError,
            main,
            args=[
                "--ifile",
                os.path.join(root_directory, "test/sample_text/invalid_file.txt"),
                "--ofile",
                os.path.join(
                    root_directory, "test/sample_text/vigenere_encoded_text.txt"
                ),
                "--cipher",
                "vigenere",
                "--key",
                os.path.join(root_directory, "test/sample_text/key.txt"),
            ],
        )

    def test_main_invalid_cipher(self):
        self.assertRaises(
            ValueError,
            main,
            args=[
                "--ifile",
                os.path.join(
                    root_directory,
                    "test/sample_text/vigenere_encoded_text_for_test.txt",
                ),
                "--ofile",
                os.path.join(
                    root_directory, "test/sample_text/vigenere_encoded_text.txt"
                ),
                "--cipher",
                "caesar",
                "--key",
                os.path.join(root_directory, "test/sample_text/key.txt"),
            ],
        )

    def test_main_decode_mode_with_invalid_key(self):
        self.assertRaises(
            ValueError,
            main,
            args=[
                "--ifile",
                os.path.join(
                    root_directory,
                    "test/sample_text/vigenere_encoded_text_for_test.txt",
                ),
                "--ofile",
                os.path.join(
                    root_directory, "test/sample_text/vigenere_encoded_text.txt"
                ),
                "--cipher",
                "caesar",
                "--decode",
                False,
                "--key",
                os.path.join(root_directory, "test/sample_text/invalid_key.txt"),
            ],
        )


if __name__ == "__main__":
    unittest.main()

import secrets
from typing import Callable, Dict
import unittest
import numpy as np
import os
from ciphers.feistel import (
    text_to_binary,
    binary_to_text,
    generate_new_feistel_block,
    perform_feistel_coding,
    feistel_main,
    generate_subkeys,
)

default_err_msg = "{} has not returned correct output"
brown_fox_text = "The quick brown fox jumps over the lazy dog!"
simple_pharse = "the"
simple_pharse_as_binary = np.array(
    [0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1]
)
root_directory = os.getcwd()


class feistel_tester(unittest.TestCase):
    def numpy_array_equality_tester(
        self,
        func: Callable,
        func_kwargs: Dict[str, any],
        expected_array: np.array,
        err_message: str,
    ) -> None:
        with self.subTest(err_message):
            (
                np.testing.assert_equal(func(**func_kwargs), expected_array),
                None,
            )

    def test_text_to_binary(self):
        self.numpy_array_equality_tester(
            func=text_to_binary,
            func_kwargs={"text": simple_pharse},
            expected_array=simple_pharse_as_binary,
            err_message="text_to_binary",
        )

    def test_binary_to_text(self):
        self.numpy_array_equality_tester(
            func=binary_to_text,
            func_kwargs={"binary": simple_pharse_as_binary},
            expected_array=simple_pharse,
            err_message="binary_to_text",
        )

    def test_split_into_left_right_blocks(self):
        left, right = np.split(text_to_binary(simple_pharse), 2)
        self.assertEqual(
            left.size,
            simple_pharse_as_binary.size / 2,
            default_err_msg.format("split_into_left_right_blocks"),
        )
        self.assertEqual(
            right.size,
            simple_pharse_as_binary.size / 2,
            default_err_msg.format("split_into_left_right_blocks"),
        )
        self.assertEqual(
            left.size,
            right.size,
            default_err_msg.format("split_into_left_right_blocks"),
        )

        left, right = np.split(text_to_binary(brown_fox_text), 2)
        self.assertEqual(
            left.size,
            right.size,
            default_err_msg.format("split_into_left_right_blocks"),
        )

    def test_generate_key(self):
        # check key is deterministic
        key1 = generate_subkeys(secret_key=0, length=10, num_blocks=2)
        key2 = generate_subkeys(secret_key=1, length=10, num_blocks=2)
        self.numpy_array_equality_tester(
            func=generate_subkeys,
            func_kwargs={"secret_key": 0, "length": 10, "num_blocks": 2},
            expected_array=key1,
            err_message=default_err_msg.format("generate_key"),
        )
        with self.assertRaises(AssertionError):
            np.testing.assert_equal(key1, key2)

    def test_generate_new_feistel_block(self):
        left, right = np.array([1, 0, 1, 0]), np.array([1, 1, 0, 0])
        secret_key = 1
        sub_key = generate_subkeys(secret_key, length=4, num_blocks=1)[0]

        expected_left = right
        expected_right = np.bitwise_xor(left, np.bitwise_xor(right, sub_key))

        self.numpy_array_equality_tester(
            func=generate_new_feistel_block,
            func_kwargs={
                "left": np.array(
                    [
                        1,
                        0,
                        1,
                        0,
                    ]
                ),
                "right": np.array(
                    [
                        1,
                        1,
                        0,
                        0,
                    ]
                ),
                "sub_key": sub_key,
            },
            expected_array=np.array([expected_left, expected_right]),
            err_message=default_err_msg.format("generate_new_feistel_block"),
        )

    def test_perform_feistel_encoding(self):
        left, right = np.array([1, 0, 1, 0]), np.array([1, 1, 0, 0])
        secret_key = 1
        sub_keys = generate_subkeys(secret_key, length=4, num_blocks=1)

        expected_right = right
        expected_left = np.bitwise_xor(left, np.bitwise_xor(right, sub_keys[0]))

        self.numpy_array_equality_tester(
            func=perform_feistel_coding,
            func_kwargs={
                "text_as_binary": np.array(
                    [
                        1,
                        0,
                        1,
                        0,
                        1,
                        1,
                        0,
                        0,
                    ]
                ),
                "subkeys": sub_keys,
            },
            expected_array=np.concatenate((expected_left, expected_right)),
            err_message=default_err_msg.format("perform_feistel_encoding"),
        )


if __name__ == "__main__":
    unittest.main()

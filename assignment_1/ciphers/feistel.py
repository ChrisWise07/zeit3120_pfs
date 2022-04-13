import random
import string
import sys
from typing import Tuple
import numpy as np


def text_to_binary(text: str) -> np.ndarray:
    return np.array(
        [bit for bit in "".join(format(ord(c), "08b") for c in text)]
    ).astype(np.uint8)


def binary_to_text(binary: np.ndarray) -> str:
    binary = binary.astype(str)

    return "".join(
        chr(int("".join(binary[i : i + 8]), 2)) for i in range(0, len(binary), 8)
    )


def generate_subkeys(secret_key: int, length: int, num_blocks: int) -> np.ndarray:
    """
    Generate subkey.
    """
    return np.random.default_rng(secret_key).integers(
        2, size=(num_blocks, length), dtype=np.uint8
    )


def generate_new_feistel_block(
    left: np.ndarray,
    right: np.ndarray,
    sub_key: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate new feistel block.
    """
    return right, np.bitwise_xor(np.bitwise_xor(right, sub_key), left)


def perform_feistel_coding(
    text_as_binary: np.ndarray, subkeys: np.ndarray
) -> np.ndarray:
    """
    Encrypt text.
    """
    left, right = np.split(text_as_binary, 2)

    for subkey in subkeys:
        left, right = generate_new_feistel_block(left, right, subkey)

    return np.concatenate((right, left))


def feistel_main(
    text: str, decode: bool, secret_key: str = None, num_blocks: int = 4
) -> np.ndarray:
    """
    Encrypt text.
    """
    if secret_key is None:
        secret_key = "".join(
            random.SystemRandom().choice(string.ascii_uppercase + string.digits)
            for _ in range(32)
        )
        print(
            f"---IMPORTANT---\n"
            f"No key was provided, so generating one for you. Please record the key\n"
            f"---IMPORTANT---\n\n"
            f"-----BEGIN FEISTEL KEY-----\n"
            f"{secret_key}\n"
            f"-----END FEISTEL KEY-----\n\n"
        )

    text_as_binary = text_to_binary(text)

    subkeys = generate_subkeys(
        int.from_bytes(secret_key.encode(), byteorder=sys.byteorder),
        text_as_binary.size // 2,
        num_blocks,
    )
    if decode:
        subkeys = np.flip(subkeys, axis=0)

    return binary_to_text(perform_feistel_coding(text_as_binary, subkeys))

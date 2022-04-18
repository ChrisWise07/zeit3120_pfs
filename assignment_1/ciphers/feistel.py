import random
import string
import sys
from typing import Tuple
import numpy as np
from .utils import file_handler

output_for_file = (
    "-----BEGIN FEISTEL KEY-----\n"
    "{key}\n"
    "-----END FEISTEL KEY-----\n\n"
    "-----BEGIN {mode} TEXT-----\n"
    "{text}\n"
    "-----END {mode} TEXT-----\n"
)


def text_to_binary(text: str) -> np.ndarray:
    """
    Convert text to binary.
    
    Args:
        text: Text to convert.
    
    Returns:
        Binary representation of text.
    """
    return np.array(
        [bit for bit in "".join(format(ord(c), "08b") for c in text)]
    ).astype(np.uint8)


def binary_to_text(binary: np.ndarray) -> str:
    """
    Convert binary to text.

    Args:
        binary: Binary to convert.

    Returns:
        Text representation of binary.
    """
    binary = binary.astype(str)

    return "".join(
        chr(int(f"0b{''.join(binary[i : i + 8])}", 2)) for i in range(0, len(binary), 8)
    )


def generate_subkeys(secret_key: int, length: int, num_blocks: int) -> np.ndarray:
    """
    Generate subkeys

    Args:
        secret_key: Secret key.
        length: Length of subkey.
        num_blocks: Number of subkeys.
    
    Returns:
        Subkeys.
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

    Args:
        left: Left part of feistel block.
        right: Right part of feistel block.
        sub_key: Subkey.
    
    Returns:
        New feistel block split into new left and right blocks.
    """
    return right, np.bitwise_xor(np.bitwise_xor(right, sub_key), left)


def perform_feistel_coding(
    text_as_binary: np.ndarray, subkeys: np.ndarray
) -> np.ndarray:
    """
    Perform feistel coding.

    Args:
        text_as_binary: Text to encode.
        subkeys: Subkeys.
    
    Returns:
        Encoded text.
    """
    left, right = np.split(text_as_binary, 2)

    for subkey in subkeys:
        left, right = generate_new_feistel_block(left, right, subkey)

    return np.concatenate((right, left))


def feistel_main(
    text: str,
    ofile: str,
    key: str = None,
    decode: bool = True,
    num_blocks: int = 4,
    **kwargs,
) -> np.ndarray:
    """
    Main function for feistel cipher.

    Args:
        text: Text to encode/decode.
        ofile: Output file.
        key: Secret key.
        decode: Decode or encode.
        num_blocks: Number of blocks.
        kwargs: Keyword arguments.
    
    Returns:
        Encoded/decoded text.
    """
    if key is None:
        key = "".join(
            random.SystemRandom().choice(string.ascii_uppercase + string.digits)
            for _ in range(32)
        )
        print(
            f"---IMPORTANT---\n"
            f"No key was provided, so generating one for you. Please record the key\n"
            f"---IMPORTANT---\n\n"
            f"-----BEGIN FEISTEL KEY-----\n"
            f"{key}\n"
            f"-----END FEISTEL KEY-----\n\n"
        )

    text_as_binary = text_to_binary(text)

    subkeys = generate_subkeys(
        int.from_bytes(key.encode(), byteorder=sys.byteorder),
        text_as_binary.size // 2,
        num_blocks,
    )

    if decode:
        subkeys = np.flip(subkeys, axis=0)
        mode_as_word = "DECODED"
    else:
        mode_as_word = "ENCODED"

    text = binary_to_text(perform_feistel_coding(text_as_binary, subkeys))

    output = output_for_file.format(
        key=key,
        mode=mode_as_word,
        text=binary_to_text(perform_feistel_coding(text_as_binary, subkeys)),
    )

    if ofile:
        file_handler(path=ofile, mode="w", func=lambda f: f.write(output))
    else:
        print(output)

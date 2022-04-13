import argparse
import os
import sys
from typing import List
from cipher_modules_map import cipher_modules_map
from ciphers.utils import file_handler


def parse_args(args) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Decoder Encoder settings")

    parser.add_argument(
        "--ifile",
        type=str,
        default=None,
        help="path to input file with text to encode/decode (default=None)",
    )
    parser.add_argument(
        "--ofile",
        type=str,
        default=None,
        help=(
            "path to output file with text that is encoded/decoded (default=None) "
            "Note: if --of is not specified, the output will be printed to stdout"
        ),
    )
    parser.add_argument(
        "--decode",
        type=bool,
        default=True,
        help="decode the input file if true else the input file is encoded(default=True)",
    )
    parser.add_argument(
        "--cipher",
        type=str,
        default="vigenere",
        help="the ciper to use (default=vigenere)",
    )
    parser.add_argument(
        "--key",
        type=str,
        default=None,
        help="path to the key file (default=None)",
    )

    return parser.parse_args(args)


def perform_checks(args):
    if args.ifile is None:
        raise ValueError("No input file specified")
    if not (os.path.exists(args.ifile)):
        raise ValueError("Input file does not exist or the path provided is incorrect")
    if not (args.cipher in cipher_modules_map):
        raise ValueError("Invalid cipher specified or cipher is not supported yet")
    if not (args.decode) and args.key is None:
        raise ValueError("No key specified for encode mode")
    if args.key and not (os.path.exists(args.key)):
        raise ValueError("Key file does not exist or the path provided is incorrect")


def main(args: List[str]) -> None:
    args = parse_args(args)

    perform_checks(args)

    if args.key:
        args.key = file_handler(path=args.key, mode="r", func=lambda f: f.read())

    cipher_modules_map[args.cipher](
        file_handler(path=args.ifile, mode="r", func=lambda f: f.read()),
        args.ofile,
        args.key,
        args.decode,
    )


if __name__ == "__main__":
    main(args=sys.argv[1:])

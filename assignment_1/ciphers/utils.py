def file_handler(path, mode, func):
    """
    This function is used to read the file and return the content of / write content to the file

    Args:
        path: path to the file
        mode: mode to open the file in
        func: function to perform on the file

    Returns:
        content of the file
    """
    try:
        with open(path, mode) as f:
            return func(f)
    except FileNotFoundError:
        return 0


output_for_file = (
    "-----BEGIN {cipher} KEY-----\n"
    "{key}\n"
    "-----END {cipher} KEY-----\n\n"
    "-----BEGIN {mode} TEXT-----\n"
    "{text}\n"
    "-----END {mode} TEXT-----\n"
)

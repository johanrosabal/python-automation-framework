import base64


def decode_base64(string: str):
    """
     Decodes a base64-encoded string.

    :param string: Base64-encoded string.
    :return: Decoded string.
    """
    try:
        decoded_data = base64.b64decode(string).decode('utf-8')
        return decoded_data
    except Exception as e:
        return f"Error decoding: {e}"


# Example
# encoded_data = "SGVsbG8gd29ybGQh"
# print(decode_base64(encoded_data))


def encode_base64(string: str):
    """
     Encode a string in base64.

    :param string: String to codify.
    :return: Base64-encoded string.
    """
    try:
        return base64.b64encode(string.encode('utf-8')).decode('utf-8')
    except Exception as e:
        return f"Error coding: {e}"

# Example
# data = "Hello world!"
# print(encode_base64(data))

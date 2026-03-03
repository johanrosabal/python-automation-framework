import random


def generate_random_code(prefix: str = None, start: int = 1000, end: int = 9999):
    """
    Generate a random code with a given prefix.
    The random number will be between 10000 and 99999.

    :param prefix: The prefix to be added to the code.
    :param start: Integer Number Initial Range
    :param end: Integer Number End Range
    :return: The generated code with the prefix.
    """

    text = ""
    if prefix is not None:
        text = f"{prefix}-"

    random_number = random.randint(start, end)  # Generate a random number between 10000 and 99999
    return f"{text}{random_number:05d}"


def replace_random_value(text_value):

    # Search for the pattern "{Random-X}" in the string
    if "{Random-" in text_value:
        # Get the numeric value after "Random-"
        start_idx = text_value.find("{Random-") + len("{Random-")
        end_idx = text_value.find("}", start_idx)
        length = int(text_value[start_idx:end_idx])  # Extract the number X which specifies the length

        # Generate a random number with the specified length
        random_value = ''.join([str(random.randint(0, 9)) for _ in range(length)])

        # Replace the "{Random-X}" pattern with the generated random value
        return text_value.replace(f"{text_value[start_idx - 8:end_idx + 1]}", random_value)

    return text_value

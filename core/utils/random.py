import random


def generate_random_code(prefix):
    """
    Generate a random code with a given prefix.
    The random number will be between 10000 and 99999.

    :param prefix: The prefix to be added to the code.
    :return: The generated code with the prefix.
    """
    random_number = random.randint(10000, 99999)  # Generate a random number between 10000 and 99999
    return f"{prefix}-{random_number:05d}"


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

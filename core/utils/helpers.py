import os


def extract_json_keys(data):
    """
       Extract unique keys from a list of dictionaries.

       :param data: A list of dictionaries.
       :return: A list of unique keys.
       """
    try:
        if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
            raise ValueError("Input must be a list of dictionaries.")

        keys = {key for item in data for key in item.keys()}
        return list(keys)
    except ValueError as e:
        print(e)


def get_file_path(file_name: str):
    # Get the current directory of the test file
    # Construct the path to file in the 'data' folder
    file_path = os.path.join('..', 'data', 'sources', file_name)  # Adjust the file name if needed
    return file_path

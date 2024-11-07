import json
import textwrap
import os
from core.config.logger_config import setup_logger

logger = setup_logger('Helpers')


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


def print_json(title: str = None, data=None, max_width=150):
    if data:
        try:
            data2 = json.loads(data)
            json_str = json.dumps(data2, indent=4)
            logger.info(title.upper())
            logger.info("+" + "-" * max_width + "+")
            for line in json_str.splitlines():
                wrapped_lines = textwrap.wrap(line, width=max_width - 4)
                for wrapped_line in wrapped_lines:
                    logger.info(f"| {wrapped_line:<{max_width - 2}} |")
            logger.info("+" + "-" * max_width + "+")
        except json.JSONDecodeError as e:
            print(f"Error JSON: {e}")
    else:
        logger.info("Data is empty.")


def generate_directory_tree(directory_path, prefix=""):
    """Generates a text-based tree of files and folders"""
    files_and_folders = os.listdir(directory_path)
    files_and_folders.sort()

    for index, name in enumerate(files_and_folders):
        current_path = os.path.join(directory_path, name)
        is_last = (index == len(files_and_folders) - 1)

        # Ignore the __pycache__ directory
        if name == "__pycache__":
            continue

        # Ignore the __init__.py file
        if name == "__init__.py":
            continue

        if name == ".git":
            continue

        if name == ".idea":
            continue

        if name == ".pytest_cache":
            continue

        # Display the structure
        if os.path.isdir(current_path):
            print(f"{prefix}|-- {name}/")
            new_prefix = f"{prefix}|   " if not is_last else f"{prefix}    "
            generate_directory_tree(current_path, new_prefix)
        else:
            print(f"{prefix}|-- {name}")


# Path of the directory you want to generate the tree for
root_directory = "../../"  # Change to your project directory
# generate_directory_tree(root_directory)

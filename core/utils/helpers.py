import json
import textwrap
import os
import time
import glob
from pathlib import Path
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


def get_file_path(file_name=""):
    """
    Retrieve JSON files from root directory and subfolders,
    filtering by files containing a specific path segment.
    """
    from pathlib import Path
    import os

    # Getting Project Root
    root = Path(__file__).parent.parent.parent.resolve()
    filtered_files = []
    root = os.path.abspath(root)  # Convert relative path to absolute path

    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith(".json"):
                file_path = os.path.join(dirpath, filename)
                if file_name in file_path.replace("\\", "/"):  # Normalize paths for filtering
                    filtered_files.append(file_path)
    if filtered_files:
        return filtered_files[0]
    else:
        logger.error(f"File {file_name} Not Found")
        return None


def wait_for_file_to_download(filename: str, timeout: int = 30, interval: int = 1):
    """
    Wait for a file to appear in the download directory.

    Arguments:
    filename (str): Name of the file to wait for.
    timeout (int): Maximum wait time in seconds (default: 30).
    interval (int): Wait interval between checks (default: 1 second).

    Returns:
    bool: True if the file exists within the timeout, False otherwise.
    """
    project_root = Path(__file__).parent.parent.parent
    download_path = f"{project_root}\\downloads"

    file_path = os.path.join(download_path, filename)
    start_time = time.time()

    while time.time() - start_time < timeout:
        if os.path.exists(file_path):
            logger.info(f"The file {filename} has been downloaded successfully.")
            return True
        time.sleep(interval)
    logger.error(f"Timed out. File {filename} not found.")
    return False


wait_for_file_to_download("samplefile.pdf", 30, 1)
# Path of the directory you want to generate the tree for
root_directory = "../../"  # Change to your project directory
# generate_directory_tree(root_directory)

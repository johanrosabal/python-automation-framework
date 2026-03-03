import json
import textwrap
import os
import time
import re
from datetime import timedelta, datetime
from pathlib import Path
from core.config.logger_config import setup_logger
import xml.etree.ElementTree as ET
from typing import Optional

import pytz
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


def print_json(title: str = "Title", data=None, max_width=150):
    """
    Prints a formatted JSON output with a title.

    If 'data' is a dictionary, it is converted to JSON.
    If 'data' is already a JSON string, it is loaded and formatted.

    :param title: Title of the JSON output.
    :param data: Data to print (can be a dictionary or JSON string).
    :param max_width: Maximum width for formatting the output.
    """
    if data:
        try:
            # Check if data is a dictionary, convert it to JSON if needed
            if isinstance(data, dict):
                json_str = json.dumps(data, indent=4)
            else:
                # If data is already a string, attempt to parse it
                json_str = json.dumps(json.loads(data), indent=4)

            # Print title if provided
            if title:
                logger.info(title.upper())

            # Print formatted JSON with a box
            logger.info("+" + "-" * max_width + "+")
            for line in json_str.splitlines():
                wrapped_lines = textwrap.wrap(line, width=max_width - 4)
                for wrapped_line in wrapped_lines:
                    logger.info(f"| {wrapped_line:<{max_width - 2}} |")
            logger.info("+" + "-" * max_width + "+")

        except json.JSONDecodeError as e:
            logger.error(f"JSON Decode Error: {e}")
    else:
        logger.info("Data is empty.")


def save_text_to_file(text: str, filename: str = "text.json") -> None:
    """
    Saves the provided response data as a JSON file.

    :param text: The data to be saved in JSON format.
    :param filename: The path where the file will be created (default is 'text.json').
    """
    project_root = Path(__file__).parent.parent.parent
    file_path = os.path.join(project_root, filename)

    # Verify if Directory exist
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(json.loads(text), file, indent=4, ensure_ascii=False)
        logger.info(f"✅ Data successfully saved to {file_path}")
    except Exception as e:
        logger.error(f"❌ Error saving data to {file_path}: {e}")


# Example
# response_data = {
#     "itemId": "123",
#     "itemDescription": "Widget",
#     "itemPrice": 100
# }
#
# save_response_to_file(response_data, filename="applications\\api\\loadiq\\tests\\loadboard\\responses\\LD25031100027_step_4.json")


def save_request_and_response(base_path: str, response, filename_prefix: str = "data") -> None:
    """
    Save request and response JSON texts into separate folders under a base path.

    :param base_path: Root directory where 'requests' and 'response' folders will be created.
    :param response: Response object containing request and response data.
    :param filename_prefix: Common prefix for the filenames (default is 'data').
    """
    project_root = Path(__file__).parent.parent.parent
    request_path = os.path.join(project_root, base_path, "requests", f"{filename_prefix}_request.json")
    response_path = os.path.join(project_root, base_path, "response", f"{filename_prefix}_response.json")

    files_to_save = []

    if isinstance(response, dict):
        if response["request"] is not None:
            files_to_save.append((request_path, response["request"]))
        else:
            logger.warning("⚠️ Request body is None. Skipping request file save.")
    else:
        if response.request.body is not None:
            files_to_save.append((request_path, response.request.body))
        else:
            logger.warning("⚠️ Request body is None. Skipping request file save.")

    if isinstance(response, dict):
        if str(response["response"].text):
            files_to_save.append((response_path, response["response"].text))
    else:

        if response.text:
            files_to_save.append((response_path, response.text))
        else:
            logger.warning("⚠️ Response text is empty. Skipping response file save.")

    for path, content in files_to_save:
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        try:
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(json.loads(content), file, indent=4, ensure_ascii=False)
            logger.info(f"✅ Data successfully saved to {path}")
        except Exception as e:
            logger.error(f"❌ Error saving data to {path}: {e}")


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


def get_relative_file_path(relative_path: str):
    """
    Get the absolute path of a file based on a relative path from the project root.

    :param relative_path: Relative path to the file from the project root (e.g., 'applications/web/loadiq/data/user_management_api/create_user.json')
    :return: Absolute path to the file or None if not found
    """
    root = Path(__file__).parent.parent.parent.resolve()
    file_path = root / relative_path

    if file_path.exists():
        return str(file_path)
    else:
        logger.error(f"File not found at relative path: {relative_path}")
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


# wait_for_file_to_download("sample_file.pdf", 30, 1)
# Path of the directory you want to generate the tree for
# root_directory = "../../"  # Change to your project directory
# generate_directory_tree(root_directory)

def generate_future_date(days_in_future: int = 0, formatDate="%m/%d/%Y"):
    """
    Generates a future date starting from today by adding the specified days.

    :param formatDate: Specify the Date Output Format
    :param days_in_future: Number of days to add to the current date.
    :return: Future date in 'YYYY-MM-DD' format.

    Use:
    days_to_add = 10
    future_date = generate_future_date(days_to_add)
    print(f"Future Date (en {days_to_add} días): {future_date}")
    """
    # Get the current date
    today = datetime.now()

    # Add the days to the argument
    future_date = today + timedelta(days=days_in_future)

    # Return the date in 'YYYY-MM-DD' format
    return future_date.strftime(formatDate)


def generate_future_datetime(hours: int = 0, minutes: int = 0, days: int = 0, format_datetime="%m/%d/%Y %H:%M"):
    """
    Generates a future datetime starting from now by adding the specified hours, minutes, and days.

    :param hours: Number of hours to add to the current datetime.
    :param minutes: Number of minutes to add to the current datetime.
    :param days: Number of days to add to the current datetime.
    :param format_datetime: Specify the DateTime Output Format (default: "MM/DD/YYYY HH:MM AM/PM")
    :return: Future datetime in specified format.

    Use:
    future_datetime = generate_future_datetime(hours=2, minutes=30)
    print(f"Future DateTime: {future_datetime}")
    """
    # Get the current datetime
    now = datetime.now()

    # Add the hours, minutes, and days
    future_datetime = now + timedelta(days=days, hours=hours, minutes=minutes)

    # Return the datetime in specified format
    return future_datetime.strftime(format_datetime)


def extract_days_from_string(date_str: str) -> int:
    """
    Extracts the number from a string like 'future-date-{5}'.

    :param date_str: The input string containing the future date format.
    :return: Extracted number as an integer.
    """
    match = re.search(r"\{(\d+)\}", date_str)  # Extract the number inside {}
    return int(match.group(1)) if match else 0  # Return the number, or 0 if not found


# str_time = "01:30 AM"
# str_date = "future-date-{4} "
# days_to_add = extract_days_from_string(str(str_date))  # Extracts 4


def next_monday_in_future_days(days=30):
    # Get the date in 15 days
    future_date = datetime.today() + timedelta(days=days)

    # Adjust to be Monday (0 = Monday, 6 = Sunday)
    days_to_monday = (7 - future_date.weekday()) % 7  # If it is already Monday, it is kept
    next_monday = future_date + timedelta(days=days_to_monday)

    return next_monday.strftime("%m/%d/%Y")  # Return in YYYY-MM-DD format


# print(next_monday_in_future_days(10))


def convert_date_format(date_str: str, formatDate: str = "%d/%m/%Y", outputFormatDate: str = "%Y-%m-%dT00:00:00.000Z"):
    """
    Converts a date from 'DD/MM/YYYY' to 'YYYY-MM-DDT00:00:00.000Z' (ISO 8601).

    :param outputFormatDate: Format the output date
    :param formatDate: Format date input
    :param date_str: Date in 'DD/MM/YYYY' format.
    :return: Date in 'YYYY-MM-DDT00:00:00.000Z' format.
    """
    dt = datetime.strptime(date_str, formatDate)  # Parse input format
    return dt.strftime(outputFormatDate)  # Convert to ISO format


def convert_date_format_to_iso8601(date_str: str, time_str: str) -> str:
    """
    Converts 'MM/DD/YYYY hh:mm AM/PM' to 'YYYY-MM-DDTHH:MM:SS.000Z' (ISO 8601).

    :param time_str: Time string for HOUR:MINUTES:INDICATOR
    :param date_str: Date string in 'MM/DD/YYYY hh:mm AM/PM' format.
    :return: Date string in 'YYYY-MM-DDTHH:MM:SS.000Z' format.
    """
    dt = datetime.strptime(f"{date_str} {time_str}", "%m/%d/%Y %I:%M %p")
    return dt.strftime("%Y-%m-%dT%H:%M:00.000Z")  # Convert to ISO format


def convert_to_24_hour(time_str: str) -> str:
    """
    Converts time from 12-hour format (HH:MM AM/PM) to 24-hour format (HH:MM).
    """
    return datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M")


# print(convert_dare_format_to_iso8601(generate_future_date(days_to_add), str_time))

# Mapping common timezone names to valid identifiers in pytz
TIMEZONE_MAPPING = {
    "Eastern Standard Time": "America/New_York",
    "Central Standard Time": "America/Costa_Rica",
    "Mountain Standard Time": "America/Denver",
    "Pacific Standard Time": "America/Los_Angeles",
    "UTC": "UTC"
}


def convert_to_utc(date_str, local_tz_name) -> str:
    """
    Converts a date string from 'MM/DD/YYYY hh:mm AM/PM' format in a given local timezone
    to UTC format 'YYYY-MM-DDTHH:MM:SS+00:00', without using `pytz`.

    :param date_str: Date string in 'MM/DD/YYYY hh:mm AM/PM' format.
    :param local_tz_name: Timezone name (e.g., 'Eastern Standard Time').
    :return: Date string in UTC format 'YYYY-MM-DDTHH:MM:SS+00:00'.
    """
    try:
        tz_name = TIMEZONE_MAPPING.get(local_tz_name, local_tz_name)
        local_tz = pytz.timezone(tz_name)

        # Convert to datetime object (naive)
        local_dt = datetime.strptime(date_str, "%m/%d/%Y %I:%M %p")

        # Localize to the specified timezone (automatically adjusts for DST)
        local_dt = local_tz.localize(local_dt)

        # Convert to UTC
        utc_dt = local_dt.astimezone(pytz.utc)

        return utc_dt.isoformat()
    except Exception as e:
        return f"Error: {e}"


# date_input = "03/14/2025 12:00 AM"
# local_timezone = "Central Standard Time"  # Replace with your actual timezone
# utc_date = convert_to_utc(date_input, local_timezone)
# print(utc_date)  # Output: 2025-03-14T06:00:00+00:00


def format_phone_number(phone: str) -> str:
    """
    Formats a 10-digit phone number into (XXX) XXX-XXXX.

    :param phone: The phone number as a string or integer.
    :return: Formatted phone number as (XXX) XXX-XXXX.
    """
    if not phone:  # Check if phone is None or empty
        return phone  # Return the original value if invalid

    if len(phone) != 10 or not phone.isdigit():  # Check if it's exactly 10 digits and contains only digits
        return phone  # Return the original value if invalid

    return f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"


# Function to process the dynamic values in the JSON
def parse_dynamic_dates_values(data: dict) -> dict:
    """
    Iterates over the input JSON and replaces dynamic fields
    EXAMPlE:
    Look for the 'future-date-{1}' pattern
    Look for the 'timestamp-prefix{CustCont}'
    Look for the 'timestamp-prefix{CustCont}'

    Takes JSON Strings Values with these Patterns and replace it with the corresponding function

    :param data: The input JSON.
    :return: The JSON with the dynamic values processed.
    """
    # Iterate over each key and value in the dictionary
    for key, value in data.items():
        if isinstance(value, dict):  # If it's a dictionary, call recursively
            data[key] = parse_dynamic_dates_values(value)
        elif isinstance(value, list):  # If it's a list, process each element
            data[key] = [parse_dynamic_dates_values(item) if isinstance(item, dict) else item for item in value]
        elif isinstance(value, str):  # If it's a string, check for dynamic values to replace
            match_future_date = re.match(r"future-date-\{(\d+)\}", value)  # Look for the 'future-date-{1}' pattern
            if match_future_date:
                days_to_add = int(match_future_date.group(1))
                future_date = generate_future_date(days_to_add)
                data[key] = re.sub(r"future-date-\{\d+\}", future_date, value)

            match_future_date = re.match(r"future-date-to-utc\{(\d+)\}", value)  # Look for the 'future-date-to-utc{1}'' pattern
            if match_future_date:
                days_to_add = int(match_future_date.group(1))
                future_date = generate_future_date(days_to_add)
                date = re.sub(r"future-date-to-utc\{\d+\}", future_date, value)
                data[key] = convert_date_format(date, "%m/%d/%Y", "%Y-%m-%dT00:00:00Z")

            timestamp_prefix = re.match(r"timestamp-prefix\{(.+?)\}", value)  # Look for the 'timestamp-prefix{CustCont}' pattern
            if timestamp_prefix:
                prefix = timestamp_prefix.group(1)
                data[key] = generate_timestamp_with_prefix(prefix)

    return data


def to_camel_case(snake_str: str, uppercase_exceptions: list = None) -> str:
    """
    Converts snake_case to camelCase, allowing certain words to stay uppercase.

    :param snake_str: The snake_case string to convert.
    :param uppercase_exceptions: List of words that should remain uppercase.
    :return: Converted camelCase string.
    """
    if "_" not in snake_str:
        return snake_str  # ✅ If there is no "_", it remains the same.

    if uppercase_exceptions is None:
        uppercase_exceptions = []

    parts = snake_str.split("_")

    parts[0] = parts[0].lower()  # ✅ Keeps the first element in lowercase

    for i in range(1, len(parts)):
        if parts[i].upper() in uppercase_exceptions:
            parts[i] = parts[i].upper()
        else:
            parts[i] = parts[i].capitalize()

    return "".join(parts)


def generate_timestamp_with_prefix(prefix):
    """
    # Example
    # prefix = "CustCont"
    # timestamp = generate_timestamp(prefix)
    # print(timestamp)
    :param prefix:
    :return: String CustCont250513213947
    """

    now = datetime.now()

    timestamp = now.strftime("%y%m%d%H%M%S")

    result = f"{prefix}{timestamp}"

    return result


def get_test_case_data_by_id(json_data: dict, test_case_id: str):
    """
    Given a loaded JSON and a test_case_id, return the data of the matching test case.
    :param json_data: Dictionary containing the test cases (already loaded from JSON)
    :param test_case_id: The test case ID to search for (e.g., 'CT-2883')
    :return: Dictionary of test case data or None if not found
    """
    for test_case in json_data.get("tests", []):
        if test_case.get("idTC") == test_case_id:
            return test_case.get("data")
    logger.warning(f"Test data for {test_case_id} not found in JSON")
    return None


def extract_test_id(path: str) -> str:
    """Extract the Test Case ID from a file Name into Path String"""
    import re
    match = re.search(r"(CT-\d+)", path)
    return match.group(1) if match else path.split("/")[-1].split(".")[0]


def safe_get(dictionary, *keys):
    """
    Accede de forma segura a claves anidadas en un diccionario.
    Devuelve None si alguna clave no existe.

    Ejemplo:
        d = {'a': {'b': {'c': 42}}}
        safe_get(d, 'a', 'b', 'c')  # → 42
        safe_get(d, 'a', 'x', 'c')  # → None
    """
    for key in keys:
        if isinstance(dictionary, dict) and key in dictionary:
            dictionary = dictionary[key]
        else:
            return None
    return dictionary


def validate_date_mmddyy(value):
    """
    Validates whether a string contains a valid date in MM/DD/YY format.
    Ignores any additional text (like time) before or after the date.

    Args:
        value (str): String containing the date (e.g., '15:30 10/23/25' or '10/23/25')

    Returns:
        bool: True if a valid MM/DD/YY date is found, False otherwise.
    """
    if not isinstance(value, str):
        return False

    # Extract MM/DD/YY pattern from the string (two digits / two digits / two digits)
    match = re.search(r'\b(\d{2})/(\d{2})/(\d{2})\b', value)
    if not match:
        return False

    date_str = match.group(0)  # e.g., '10/23/25'

    try:
        # Validate structure and logical values (month 01-12, valid day for month, etc.)
        datetime.strptime(date_str, '%m/%d/%y')
        return True
    except ValueError:
        return False


def extract_date(date_string: str) -> str:
    """
    Extracts and returns only the date part in DD/MM/YYYY format
    from a string with format 'Day DD/MM/YYYY HH:MM'

    Args:
        date_string: e.g., 'Tue 12/02/2025 14:35'

    Returns:
        str: Date in 'DD/MM/YYYY' format

    Raises:
        ValueError: If the input format is invalid
    """
    try:
        # Parse the full string (%a captures the abbreviated weekday in English)
        dt = datetime.strptime(date_string.strip(), '%a %m/%d/%Y %H:%M')
        # Format only the date part
        return dt.strftime('%d/%m/%Y')
    except ValueError as e:
        raise ValueError(
            f"Invalid date format: '{date_string}'. "
            "Expected format: 'Day MM/DD/YYYY HH:MM' (e.g., 'Tue 12/02/2025 14:35')"
        ) from e


def is_date_in_range(date_to_validate: str, start_date: str, end_date: str) -> bool:
    """
    Validates if a date falls within a specified range.
    Handles dates with or without time components.
    """
    try:
        # Remove day name (e.g., "Wed ") from date_to_validate
        date_clean = date_to_validate.split(" ", 1)[-1]

        # Try parsing with time first, then without time
        for fmt_target in ["%m/%d/%Y %H:%M", "%m/%d/%Y"]:
            try:
                target = datetime.strptime(date_clean, fmt_target)
                break
            except ValueError:
                continue

        # Parse start and end dates (try with time first, then without)
        for fmt_range in ["%m/%d/%Y %H:%M", "%m/%d/%Y"]:
            try:
                start = datetime.strptime(start_date, fmt_range)
                end = datetime.strptime(end_date, fmt_range)
                break
            except ValueError:
                continue

        # Check range (inclusive)
        return start <= target <= end

    except Exception as e:
        print(f"Error: {e}")
        return False

    # # Example 1: Date within range
    # result = is_date_in_range(
    #     "Wed 12/24/2025 10:48",
    #     "12/01/2025 00:00",
    #     "12/31/2025 23:59"
    # )

    # TEST
    # result = is_date_in_range(
    #     date_to_validate="Wed 12/24/2025 10:48",
    #     start_date="12/01/2025",
    #     end_date="01/31/2026"
    # )
    # print(f"Result: {result}")  # Should print: True

import json
import textwrap
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


def print_json_response(response_json, max_width=150):
    json_str = json.dumps(response_json, indent=4)
    logger.info("RESPONSE")
    logger.info("+" + "-" * max_width + "+")
    for line in json_str.splitlines():
        wrapped_lines = textwrap.wrap(line, width=max_width - 4)
        for wrapped_line in wrapped_lines:
            logger.info(f"| {wrapped_line:<{max_width-2}} |")
    logger.info("+" + "-" * max_width + "+")


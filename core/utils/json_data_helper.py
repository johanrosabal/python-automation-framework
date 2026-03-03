"""
JSON Data Helper - Utility functions for loading and saving test data from JSON files
"""
import re

from core.config.logger_config import setup_logger
from core.data.sources.JSON_reader import JSONReader
from core.utils import helpers

logger = setup_logger('JSONDataHelper')


class JSONDataHelper:
    """Helper class for loading and saving test data from JSON files"""

    @staticmethod
    def load_json_data(filepath, test_case_id=None, key=None):
        """
        Load JSON data, optionally for a specific test case and key

        Args:
            filepath: Path to the JSON file
            test_case_id: Optional test case ID (e.g., "CT-1498")
            key: Optional key to retrieve specific value from test case data

        Returns:
            Full data if no test_case_id, test case data if test_case_id provided,
            specific value if both test_case_id and key provided

        Example:
            # Load all data
            data = JSONDataHelper.load_json_data("path/to/file.json")
            
            # Load specific test case data
            test_data = JSONDataHelper.load_json_data("path/to/file.json", "CT-2883")
            
            # Load specific key from test case
            email = JSONDataHelper.load_json_data("path/to/file.json", "CT-2883", "email")
        """
        path = helpers.get_relative_file_path(filepath)
        data = JSONReader().import_json(path)
        logger.info(f"Loaded data from {filepath}")

        # If no test case ID specified, return full data
        if test_case_id is None:
            return data

        # Find specific test case
        for test in data.get("tests", []):
            if test.get("idTC") == test_case_id:
                test_data = test.get("data", {})
                if key is None:
                    logger.info(f"Retrieved test case {test_case_id} data: {test_data}")
                    return test_data
                else:
                    value = test_data.get(key)
                    logger.info(f"Retrieved {key}={value} from test case {test_case_id}")
                    return value

        logger.warning(f"Test case {test_case_id} not found in {filepath}")
        return None

    @staticmethod
    def save_json_data(filepath, test_case_id, **data_to_save):
        """
        Save a specific value to a test case in the JSON file

        Args:
            filepath: Path to the JSON file
            test_case_id: The test case ID (e.g., "CT-1498")
            **data_to_save: Key-value pairs to save (e.g., shipment_id="123", status="active")

        Returns:
            bool: True if successful, False otherwise

        Example:
            success = JSONDataHelper.save_json_data(
                "path/to/file.json", 
                "CT-2883",
                email="new@email.com",
                firstName="John"
            )
        """
        path = helpers.get_relative_file_path(filepath)

        # Load existing data
        data = JSONReader().import_json(path)

        # Find the test case and update it
        for test in data.get("tests", []):
            if test.get("idTC") == test_case_id:
                if "data" not in test:
                    test["data"] = {}

                # Deep merge for nested dictionaries
                for key, value in data_to_save.items():
                    if isinstance(value, dict) and key in test["data"] and isinstance(test["data"][key], dict):
                        test["data"][key].update(value)  # Merge
                    else:
                        test["data"][key] = value  # Normal replacement
                break
        else:
            logger.warning(f"Test case {test_case_id} not found in {filepath}")
            return False

        # Save back to file
        try:
            import json
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            logger.info(f"Saved {data_to_save} to test case {test_case_id} in {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving data to {filepath}: {e}")
            return False

    @staticmethod
    def increment_fields_in_json(filepath, test_case_id, fields, regex_pattern=r'\d+$'):
        test_data = JSONDataHelper.load_json_data(filepath, test_case_id)
        if not test_data:
            raise ValueError("Test data not found")

        match = re.search(regex_pattern, test_data[fields[0]])
        if not match:
            raise ValueError(f"No number found in {fields[0]}")
        current_num = int(match.group())
        new_num = current_num + 1
        new_num_str = f"{new_num:03d}"

        updated_data = {}
        for field in fields:
            updated_data[field] = re.sub(regex_pattern, new_num_str, test_data[field])

        JSONDataHelper.save_json_data(filepath, test_case_id, **updated_data)


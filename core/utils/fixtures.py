import pytest

from core.config.logger_config import setup_logger

from core.data.sources.JSON_reader import JSONReader
from core.utils import helpers

logger = setup_logger('Running Fixture')

@pytest.fixture
def load_json_data():
    def _load_json_data(filepath, test_case_id=None, key=None):
        """
        Load JSON data, optionally for a specific test case and key

        Args:
            filepath: Path to the JSON file
            test_case_id: Optional test case ID (e.g., "CT-1498")
            key: Optional key to retrieve specific value from test case data

        Returns:
            Full data if no test_case_id, test case data if test_case_id provided,
            specific value if both test_case_id and key provided
        """
        path = helpers.get_relative_file_path(filepath)
        data = JSONReader().import_json(path)
        logger.info(f"[Fixture] Loaded data from {filepath}")

        # If no test case ID specified, return full data
        if test_case_id is None:
            return data

        # Find specific test case
        for test in data.get("tests", []):
            if test.get("idTC") == test_case_id:
                test_data = test.get("data", {})
                if key is None:
                    logger.info(f"[Fixture] Retrieved test case {test_case_id} data: {test_data}")
                    return test_data
                else:
                    value = test_data.get(key)
                    logger.info(f"[Fixture] Retrieved {key}={value} from test case {test_case_id}")
                    return value

        logger.warning(f"Test case {test_case_id} not found in {filepath}")
        return None

    return _load_json_data


@pytest.fixture
def save_json_data():
    def _save_json_data(filepath, test_case_id, **data_to_save):
        """
        Save a specific value to a test case in the JSON file

        Args:
            filepath: Path to the JSON file
            test_case_id: The test case ID (e.g., "CT-1498")
            **data_to_save: Key-value pairs to save (e.g., shipment_id="123", status="active")
        """
        path = helpers.get_relative_file_path(filepath)

        # Load existing data
        data = JSONReader().import_json(path)

        # Find the test case and update it
        for test in data.get("tests", []):
            if test.get("idTC") == test_case_id:
                if "data" not in test:
                    test["data"] = {}

                for key, value in data_to_save.items():
                    if isinstance(value, dict) and key in test["data"] and isinstance(test["data"][key], dict):
                        test["data"][key].update(value)  # Merge
                    else:
                        test["data"][key] = value  # Reemplazo normal
                break
        else:
            logger.warning(f"Test case {test_case_id} not found in {filepath}")
            return False
        # Save back to file
        try:
            import json
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            logger.info(f"[Fixture] Saved {data_to_save} to test case {test_case_id} in {filepath}")
            return True
        except Exception as e:
            logger.error(f"[Fixture] Error saving data to {filepath}: {e}")
            return False

    return _save_json_data
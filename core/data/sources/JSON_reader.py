import json
from tabulate import tabulate
from core.config.logger_config import setup_logger
logger = setup_logger('JSONReader')


class JSONReader:
    def __init__(self):
        """
        Initialize the JSON reader with the file path.
        """
        self.file_path = None
        self.data = None

    def set_file_path(self, file_path):
        """
        Set the JSON file path and load the data.

        :param file_path: The path file name where the file is located.
        """
        self.file_path = file_path
        return self

    def read_list_structure(self, object_class=None, nested_key=None):
        """
        Map the JSON data to a list of instances of a given class,
        using a specific field mapping.

        :param object_class: The class to which the rows will be mapped.
        :param nested_key: The key in the JSON to navigate to the nested data (e.g., 'test.new_users').
        :return: A list of instances of the specified class or the raw JSON data.
        """
        with open(self.file_path, 'r') as file:
            self.data = json.load(file)

        if object_class is None and nested_key is None:
            # Return raw JSON data if no class mapping or nested key is provided
            return self.data

        objects = []

        if nested_key:
            keys = nested_key.split('.')
            nested_data = self.data
            for key in keys:
                nested_data = nested_data.get(key, [])

            # If the nested data is a string, convert it into a list
            if isinstance(nested_data, str):
                nested_data = [nested_data]  # Convert a string to a list
        else:
            nested_data = self.data

        # Validate if we are dealing with a list or a dictionary
        if isinstance(nested_data, list):
            for item in nested_data:
                if isinstance(item, dict):
                    # Attribute mapping if the item is a dictionary
                    object_data = {attr: item.get(column_name) for column_name, attr in object_class.mapping.items()}
                    obj = object_class(**object_data)
                    objects.append(obj)
                elif isinstance(item, str):
                    # Create object directly if it is a string
                    obj = object_class(**{attr: item for attr in object_class.mapping.values()})
                    objects.append(obj)
                else:
                    logger.error(f"Expected dict or str but got {type(item)}: {item}")
        elif isinstance(nested_data, dict):
            object_data = {attr: nested_data.get(column_name) for column_name, attr in object_class.mapping.items()}
            obj = object_class(**object_data)
            objects.append(obj)
        else:
            logger.error(f"Unexpected data type: {type(nested_data)}")

        self.display_table(nested_data)
        return objects

    def read_single_structure(self, object_class=None, nested_key=None):
        """
        Map the JSON data to an instance of a given class,
        assuming the data structure is a single object (structure 2).

        :param object_class: The class to which the rows will be mapped.
        :param nested_key: The key in the JSON to navigate to the nested data (e.g., 'tests.new_users').
        :return: An instance of the specified class or the raw JSON data.
        """
        with open(self.file_path, 'r') as file:
            self.data = json.load(file)

        if object_class is None and nested_key is None:
            # Return raw JSON data if no class mapping or nested key is provided
            return self.data

        if nested_key:
            keys = nested_key.split('.')
            nested_data = self.data
            for key in keys:
                nested_data = nested_data.get(key, {})
        else:
            nested_data = self.data

        # Assuming the data is a single object
        object_data = {attr: nested_data.get(column_name) for column_name, attr in object_class.mapping.items()}
        obj = object_class(**object_data)

        # Display as a table with a single row
        self.display_table([nested_data])
        return obj

    def display_table(self, data):
        """
        Display the contents of the JSON data as a table in the console.

        :param data: The list of dictionaries or a single dictionary to be displayed.
        """
        if isinstance(data, dict):
            data = [data]  # Convert a single dictionary into a list of dictionaries

        if data:
            headers = list(data[0].keys())  # Get the keys as headers
            table = [list(item.values()) for item in data]  # Get the values of each item
            logger.info("\n" + tabulate(table, headers=headers, tablefmt='pretty'))
        else:
            logger.info("No data available. Please read the file first.")

    def get_raw_json(self):
        """
        Return the raw JSON data loaded from the file.

        :return: The raw JSON data.
        """
        return self.data

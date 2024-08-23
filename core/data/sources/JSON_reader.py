import json
from tabulate import tabulate


class JSONReader:
    def __init__(self):
        """
        Initialize the JSON reader with the file path.
        """
        self.file_path = None
        self.data = None

    def set_file_path(self, file_path):
        """
        Set the Excel file path and load the data into a pandas DataFrame.

        :param file_path: The path file name where the file is located.
        """
        self.file_path = file_path
        return self

    def read_file(self, object_class=None, nested_key=None):
        """
        Map the JSON data to a list of instances of a given class,
        using a specific field mapping.

        :param object_class: The class to which the rows will be mapped.
        :param nested_key: The key in the JSON to navigate to the nested data (e.g., 'test.new_users').
        :return: A list of instances of the specified class.
        """

        """
        Read the JSON file and load the data into a dictionary.
        """
        with open(self.file_path, 'r') as file:
            self.data = json.load(file)

        objects = []

        if nested_key:
            keys = nested_key.split('.')
            nested_data = self.data
            for key in keys:
                nested_data = nested_data.get(key, [])
        else:
            nested_data = self.data

        for item in nested_data:
            # Create a dictionary with the mapping of the row values
            object_data = {attr: item.get(column_name) for column_name, attr in object_class.mapping.items()}
            # Create an instance of the class using the mapped data
            obj = object_class(**object_data)
            objects.append(obj)

        self.display_table(nested_data)
        return objects

    def display_table(self, data):
        """
        Display the contents of the JSON data as a table in the console.

        :param data: The list of dictionaries to be displayed.
        """
        if data:
            headers = list(data[0].keys())
            table = [list(item.values()) for item in data]
            print("")
            print(tabulate(table, headers=headers, tablefmt='pretty'))
        else:
            print("No data available. Please read the file first.")
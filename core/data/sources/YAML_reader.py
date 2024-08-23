import yaml
from tabulate import tabulate


class YAMLReader:
    def __init__(self):
        """
        Initialize the YAML reader with the file path.
        """
        self.file_path = None
        self.data = None

    def set_file_path(self, file_path):
        """
        Set the YAML file path and return the instance.

        :param file_path: The path to the YAML file.
        :return: The YAMLReader instance.
        """
        self.file_path = file_path
        return self

    def read_file(self, object_class=None, nested_key=None):
        """
        Read the YAML file and map the data from a specified section to a list of instances of a given class.

        :param object_class: The class to which the rows will be mapped.
        :param section: The section of the YAML file to read (e.g., 'tests.new_users').
        :return: A list of instances of the specified class.
        """
        with open(self.file_path, 'r') as file:
            self.data = yaml.safe_load(file)

        # Accessing the specified section data from the loaded YAML
        items = self._get_nested_section(nested_key)

        objects = []
        if not items:
            raise ValueError(f"No data found in section '{nested_key}'.")

        column_mapping = object_class.mapping

        for item in items:
            # Create a dictionary with the mapping of the item values
            object_data = {attr: item.get(column_name) for column_name, attr in column_mapping.items()}
            # Create an instance of the class using the mapped data
            obj = object_class(**object_data)
            objects.append(obj)

        self.display_table(items)
        return objects

    def _get_nested_section(self, section):
        """
        Retrieve the data from a nested section using dot notation.

        :param section: The section string in dot notation (e.g., 'tests.new_users').
        :return: The data from the specified section.
        """
        keys = section.split('.')
        data = self.data

        for key in keys:
            if key in data:
                data = data[key]
            else:
                return None
        return data

    def display_table(self, items):
        """
        Display the contents of the YAML data as a table in the console.
        """
        if items:
            headers = list(items[0].keys())
            table = [list(item.values()) for item in items]
            print("")
            print(tabulate(table, headers=headers, tablefmt='pretty'))
        else:
            print("No data available. Please read the file first.")
        return self

    def get_headers(self, section=None):
        """
        Return the headers of the specified section in the YAML file.

        :return: List of headers.
        """
        items = self._get_nested_section(section)
        if items:
            return list(items[0].keys())
        return []

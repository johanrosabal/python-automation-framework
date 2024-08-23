import xml.etree.ElementTree as ET
from tabulate import tabulate

class XMLReader:
    def __init__(self):
        """
        Initialize the XML reader with the file path.
        """
        self.file_path = None
        self.root = None

    def set_file_path(self, file_path):
        """
        Set the XML file path and return the instance.

        :param file_path: The path to the XML file.
        :return: The XMLReader instance.
        """
        self.file_path = file_path
        return self

    def read_file(self, object_class=None, section=None):
        """
        Read the XML file and map the data from a specified section to a list of instances of a given class.

        :param object_class: The class to which the rows will be mapped.
        :param section: The section of the XML file to read (e.g., 'new_users').
        :return: A list of instances of the specified class.
        """
        tree = ET.parse(self.file_path)
        self.root = tree.getroot()

        # Accessing the specified section data from the loaded XML
        items = self.root.find(section)
        if items is None:
            raise ValueError(f"No section found with name '{section}'.")

        objects = []
        column_mapping = object_class.mapping

        for item in items:
            # Create a dictionary with the mapping of the item values
            object_data = {attr: item.find(column_name).text for column_name, attr in column_mapping.items()}
            # Create an instance of the class using the mapped data
            obj = object_class(**object_data)
            objects.append(obj)

        self.display_table(items)
        return objects

    def display_table(self, items):
        """
        Display the contents of the XML data as a table in the console.
        """
        if items:
            headers = [elem.tag for elem in items[0]]
            table = [[elem.text for elem in item] for item in items]
            print("")
            print(tabulate(table, headers=headers, tablefmt='pretty'))
        else:
            print("No data available. Please read the file first.")
        return self

    def get_headers(self, section=None):
        """
        Return the headers of the specified section in the XML file.

        :return: List of headers.
        """
        if self.root and section:
            section_element = self.root.find(section)
            if section_element:
                return [elem.tag for elem in section_element[0]]
        return []

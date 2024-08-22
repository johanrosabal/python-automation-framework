import pandas as pd
from tabulate import tabulate

class ExcelReader:
    def __init__(self, file_path):
        """
        Initialize the Excel reader with the file path.

        :param file_path: Path to the Excel file.
        """
        self.file_path = file_path
        self.data_frame = None

    def read_file(self, sheet_name=None):
        """
        Read the Excel file and load the data into a pandas DataFrame.

        :param sheet_name: The name of the sheet to read. If None, the first sheet is read.
        """
        self.data_frame = pd.read_excel(self.file_path, sheet_name=sheet_name)

    def map_to_objects(self, object_class, column_mapping):
        """
        Map the rows of the DataFrame to a list of instances of a given class,
        using a specific column mapping.

        :param object_class: The class to which the rows will be mapped.
        :param column_mapping: A dictionary mapping column names to class attributes.
        :return: A list of instances of the specified class.
        """
        objects = []
        for _, row in self.data_frame.iterrows():
            # Create a dictionary with the mapping of the row values
            object_data = {attr: row.get(column_name) for column_name, attr in column_mapping.items()}
            # Create an instance of the class using the mapped data
            obj = object_class(**object_data)
            objects.append(obj)
        return objects

    def get_headers(self):
        """
        Return the headers of the Excel file.

        :return: List of headers.
        """
        return list(self.data_frame.columns)

    def display_table(self):
        """
        Display the contents of the DataFrame as a table in the console.
        """
        if self.data_frame is not None:
            print(tabulate(self.data_frame, headers='keys', tablefmt='pretty'))
        else:
            print("No data available. Please read the file first.")
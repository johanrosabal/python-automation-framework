import pandas as pd
from tabulate import tabulate


class ExcelReader:
    def __init__(self):
        """
        Initialize the Excel reader with the file path.
        """
        self.file_path = None
        self.data_frame = None

    def set_file_path(self, file_path):
        """
        Set the Excel file path and load the data into a pandas DataFrame.

        :param file_path: The path file name where the file is located.
        """
        self.file_path = file_path
        return self

    def read_file(self, object_class=None, sheet_name=None):

        """
        Map the rows of the DataFrame to a list of instances of a given class,
        using a specific column mapping.

        :param object_class: The class to which the rows will be mapped.
        :param sheet_name: The name of the sheet to read. If None, the first sheet is read.
        :return: A list of instances of the specified class.
        """
        column_mapping = object_class.mapping
        self.data_frame = pd.read_excel(self.file_path, sheet_name=sheet_name)

        objects = []
        for _, row in self.data_frame.iterrows():
            # Create a dictionary with the mapping of the row values
            object_data = {attr: row.get(column_name) for column_name, attr in column_mapping.items()}
            # Create an instance of the class using the mapped data
            obj = object_class(**object_data)
            objects.append(obj)

        self.display_table()
        return objects

    def display_table(self):
        """
        Display the contents of the DataFrame as a table in the console.
        """
        if self.data_frame is not None:
            print("")
            print(tabulate(self.data_frame, headers='keys', tablefmt='pretty'))
        else:
            print("No data available. Please read the file first.")
        return self

    def get_headers(self):
        """
        Return the headers of the Excel file.

        :return: List of headers.
        """
        return list(self.data_frame.columns)

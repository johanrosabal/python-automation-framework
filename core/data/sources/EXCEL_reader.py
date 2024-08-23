import pandas as pd
from tabulate import tabulate


class EXCELReader:
    def __init__(self):
        """
        Initialize the file reader with the file path.
        """
        self.file_path = None
        self.data_frame = None

    def set_file_path(self, file_path):
        """
        Set the file path and return the instance.

        :param file_path: The path to the file.
        :return: The FileReader instance.
        """
        self.file_path = file_path
        return self

    def read_file(self, object_class=None, sheet_name=None):
        """
        Read the file (Excel or CSV) and map the rows to a list of instances of a given class.

        :param object_class: The class to which the rows will be mapped.
        :param sheet_name: The name of the sheet to read for Excel files. Ignored for CSV files.
        :return: A list of instances of the specified class.
        """
        column_mapping = object_class.mapping

        # Check the file extension to determine whether to read as Excel or CSV
        if self.file_path.endswith('.xlsx') or self.file_path.endswith('.xls'):
            self.data_frame = pd.read_excel(self.file_path, sheet_name=sheet_name)
        elif self.file_path.endswith('.csv'):
            self.data_frame = pd.read_csv(self.file_path)
        else:
            raise ValueError("Unsupported file format. Only Excel (.xlsx, .xls) and CSV files are supported.")

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
        Return the headers of the file.

        :return: List of headers.
        """
        return list(self.data_frame.columns)

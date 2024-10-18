import pandas as pd
from tabulate import tabulate
from core.config.logger_config import setup_logger
logger = setup_logger('TABTEXT_Reader')


class TABTEXT_Reader:
    def __init__(self):
        """
        Initialize the Tab-Delimited Text reader with the file path.
        """
        self.file_path = None
        self.data_frame = None

    def set_file_path(self, file_path):
        """
        Set the file path and return the instance.

        :param file_path: The path to the tab-delimited text file.
        :return: The TabDelimitedTextReader instance.
        """
        self.file_path = file_path
        return self

    def read_file(self, object_class=None):
        """
        Read the tab-delimited text file and map the rows to a list of instances of a given class.

        :param object_class: The class to which the rows will be mapped.
        :return: A list of instances of the specified class.
        """
        column_mapping = object_class.mapping

        # Read the tab-delimited text file into a pandas DataFrame
        self.data_frame = pd.read_csv(self.file_path, delimiter='\t')

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
            logger.info("\n"+tabulate(self.data_frame, headers='keys', tablefmt='pretty'))
        else:
            logger.info("No data available. Please read the file first.")
        return self

    def get_headers(self):
        """
        Return the headers of the tab-delimited text file.

        :return: List of headers.
        """
        return list(self.data_frame.columns)

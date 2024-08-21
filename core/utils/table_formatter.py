from tabulate import tabulate
from core.config.logger_config import setup_logger
from core.utils.helpers import extract_json_keys
logger = setup_logger('Delete')


class TableFormatter:
    def __init__(self):
        """
        Initialize the TableFormatter with headers and data.

        :param headers: A list of column headers for the table.
        :param data: A list of lists containing the rows of data.
        """
        self.headers = None
        self.data = None

    def set_data(self, data):
        """
        Initialize the TableFormatter with headers and data.
        :param data: A list of lists containing the rows of data.
        """
        self.data = data
        return self

    def set_headers(self, headers):
        self.headers = headers
        return self

    def to_plaintext(self):
        """
        Format the table as plain text.
        """
        table = tabulate(self.data, headers=self.headers, tablefmt="plain")
        logger.info(f"\n{table}")

    def to_grid(self):
        """
        Format the table as a grid.
        """
        table = tabulate(self.data, headers=self.headers, tablefmt="grid")
        logger.info(f"\n{table}")

    def to_fancy_grid(self):
        """
        Format the table as a fancy grid.
        """
        table = tabulate(self.data, headers=self.headers, tablefmt="fancy_grid")
        logger.info(f"\n{table}")

    def to_html(self):
        """
        Format the table as HTML.
        """
        table = tabulate(self.data, headers=self.headers, tablefmt="html")
        logger.info(f"\n{table}")

    def to_latex(self):
        """
        Format the table as LaTeX.
        """
        table = tabulate(self.data, headers=self.headers, tablefmt="latex")
        logger.info(f"\n{table}")

    def to_markdown(self):
        """
        Format the table as Markdown.
        """
        table = tabulate(self.data, headers=self.headers, tablefmt="github")
        logger.info(f"\n{table}")

    def to_rst(self):
        """
        Format the table as reStructuredText.
        """
        table = tabulate(self.data, headers=self.headers, tablefmt="rst")
        logger.info(f"\n{table}")

    def prepare_list(self, data):
        """
        Prepare the data for table formatting by extracting keys and
        creating a list of lists for each row.

        :param data: A list of dictionaries to process.
        :return: A tuple containing headers and formatted data.
        """
        if not data:
            raise ValueError("Data cannot be empty.")

        # Extract keys and set headers
        self.headers = extract_json_keys(data)

        # Prepare formatted data
        formatted_data = [[item.get(header, "") for header in self.headers] for item in data]
        self.data = formatted_data

        return self

    def prepare_single_item(self, item):
        """
        Prepare the data for table formatting from a single dictionary.

        :param item: A dictionary to process.
        :return: A tuple containing headers and formatted data.
        """
        if not isinstance(item, dict):
            raise ValueError("Input must be a dictionary.")

        # Extract keys and set headers
        self.headers = list(item.keys())

        # Prepare formatted data as a list containing one list (the row)
        formatted_data = [[item.get(header, "") for header in self.headers]]
        self.data = formatted_data
        return self


# Example usage
# if __name__ == "__main__":
    # headers = ["Name", "Age", "Occupation"]
    # data = [
    #     ["Alice", 30, "Engineer"],
    #     ["Bob", 24, "Designer"],
    #     ["Charlie", 28, "Teacher"]
    # ]
    #
    # formatter = TableFormatter(headers, data)
    # formatter.to_plaintext()
    # formatter.to_grid()
    # formatter.to_fancy_grid()
    # formatter.to_html()
    # formatter.to_latex()
    # formatter.to_markdown()
    # formatter.to_rst()
